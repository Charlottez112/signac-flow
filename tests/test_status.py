# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
import io
import operator
import os
import sys

import generate_status_reference_data as gen
import pytest
import signac
from test_project import redirect_stderr, redirect_stdout

import flow
import flow.environments


def test_env(env, monkeypatch):

    # Force asserts to show the full file when failures occur.
    # Useful to debug errors that arise.

    # Must import the data into the project.
    with signac.TemporaryProject(name=gen.PROJECT_NAME) as p:
        with gen.get_masked_flowproject(p, environment=env) as fp:
            # Here we set the appropriate executable for all the operations. This
            # is necessary as otherwise the default executable between submitting
            # and running could look different depending on the environment.
            for group in fp.groups.values():
                for op_key in group.operations:
                    if op_key in group.operation_directives:
                        monkeypatch.setitem(
                            group.operation_directives[op_key],
                            "executable",
                            gen.MOCK_EXECUTABLE,
                        )
            fp.import_from(origin=gen.ARCHIVE_DIR)
            jobs = fp.find_jobs(dict(environment=_env_name(env)))
            if not len(jobs):
                raise RuntimeError(
                    f"No reference data for environment {_env_name(env)}!"
                )
            reference = []
            generated = []
            for job in jobs:
                parameters = job.sp.parameters()
                if "bundle" in parameters:
                    bundle = parameters.pop("bundle")
                    tmp_out = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
                    with open(os.devnull, "w") as devnull:
                        with redirect_stderr(devnull):
                            with redirect_stdout(tmp_out):
                                fp.submit(
                                    jobs=[job],
                                    names=bundle,
                                    pretend=True,
                                    force=True,
                                    bundle_size=len(bundle),
                                    **parameters,
                                )
                    tmp_out.seek(0)
                    msg = f"---------- Bundled submission of job {job}"
                    generated.extend([msg] + tmp_out.read().splitlines())

                    with open(job.fn("script_{}.sh".format("_".join(bundle)))) as file:
                        reference.extend([msg] + file.read().splitlines())
                else:
                    for op in {**fp.operations, **fp.groups}:
                        if "partition" in parameters:
                            # Don't try to submit GPU operations to CPU partitions
                            # and vice versa.  We should be able to relax this
                            # requirement if we make our error checking more
                            # consistent.
                            if operator.xor(
                                "gpu" in parameters["partition"].lower(),
                                "gpu" in op.lower(),
                            ):
                                continue
                        tmp_out = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
                        with open(os.devnull, "w") as devnull:
                            with redirect_stderr(devnull):
                                with redirect_stdout(tmp_out):
                                    fp.submit(
                                        jobs=[job],
                                        names=[op],
                                        pretend=True,
                                        force=True,
                                        **parameters,
                                    )
                        tmp_out.seek(0)
                        msg = f"---------- Submission of operation {op} for job {job}."
                        generated.extend([msg] + tmp_out.read().splitlines())

                        with open(job.fn(f"script_{op}.sh")) as file:
                            reference.extend([msg] + file.read().splitlines())
            assert "\n".join(generated) == "\n".join(reference)
