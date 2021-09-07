import os

import flow
from flow import FlowProject


class _TestProject(FlowProject):
    pass


group1 = _TestProject.make_group(name="group1")
group2 = _TestProject.make_group(name="group2")


@_TestProject.label
def default_label(job):
    return True


@_TestProject.label
def negative_default_label(job):
    return False


@_TestProject.label("named_label")
def anonymous_label(job):
    return True


@_TestProject.label
def b_is_even(job):
    try:
        return job.sp.b % 2 == 0
    except AttributeError:
        return False


@flow.cmd
@group1
@_TestProject.pre(b_is_even)
@_TestProject.post.isfile("world.txt")
def op1(job):
    return 'echo "hello" > {job.ws}/world.txt'


@_TestProject.operation
@group1
@_TestProject.post.true("test")
def op2(job):
    job.document.test = os.getpid()


@_TestProject.operation
@group2
@_TestProject.post.true("test3_true")
@_TestProject.post.false("test3_false")
@_TestProject.post.not_(lambda job: job.doc.test3_false)
def op3(job):
    job.document.test3_true = True
    job.document.test3_false = False


if __name__ == "__main__":
    _TestProject().main()
