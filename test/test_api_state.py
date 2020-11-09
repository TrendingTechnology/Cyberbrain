from cyberbrain import Binding, Symbol, InitialValue, Return


def test_call_tracer_multiple_times(tracer):
    tracer.start()
    a = 1
    tracer.stop()

    tracer.start()  # This should have no effect
    a = 2
    tracer.stop()  # This should have no effect

    assert tracer.events == [
        Binding(lineno=6, target=Symbol("a"), value="1", sources=set())
    ]


def test_decorator_multiple_times(trace, rpc_stub):
    @trace
    def func(b):
        a = b
        return a

    func(1)

    # Test that server wait does not block user code execution.
    trace._wait_for_termination()

    assert func(2) == 2
    from cyberbrain import pprint

    pprint(trace.events)
    assert trace.events == [
        InitialValue(
            lineno=21,
            target=Symbol("b"),
            value="1",
        ),
        Binding(lineno=21, target=Symbol("a"), value="1", sources={Symbol("b")}),
        Return(lineno=22, value="1", sources={Symbol("a")}),
    ]

    trace.rpc_client.stop()
