from state_machine import State, acts_as_state_machine, Event, after, before, InvalidStateTransition


@acts_as_state_machine
class Process:
    """指定状态机的初始状态."""
    created = State(initial=True)
    waiting = State()
    running = State()
    terminated = State()  # 终止
    blocked = State()  # 阻塞
    swapped_out_waiting = State()
    swapped_out_blocked = State()

    """定义状态转换."""
    wait = Event(from_states=(created, running, blocked, swapped_out_waiting), to_state=waiting)
    run = Event(from_states=waiting, to_state=running)
    terminate = Event(from_states=running, to_state=terminated)
    block = Event(from_states=(running, swapped_out_blocked), to_state=blocked)
    swap_wait = Event(from_states=waiting, to_state=swapped_out_waiting)
    swap_block = Event(from_states=blocked, to_state=swapped_out_blocked)

    def __init__(self, name):
        self.name = name

    @after('wait')
    def wait_info(self):
        print(f"{self.name} entered waiting mode.")

    @after('run')
    def run_info(self):
        print(f"{self.name} is running.")

    @before('terminate')
    def terminate_info(self):
        print(f"{self.name} terminate.")

    @after('block')
    def block_info(self):
        print(f"{self.name} is block.")

    @after('swap_wait')
    def swap_wait_info(self):
        print(f"{self.name} is swapped out and waiting.")

    @after('swap_block')
    def swap_block_info(self):
        print(f"{self.name} is swapped put and blocked.")


def transition(process, event, event_name):
    """
    状态的转换.
    :param process: 进程
    :param event: 事件
    :param event_name: 事件名称
    :return:
    """
    try:
        event()
    except InvalidStateTransition as e:
        print(f"Error:transition of {process.name} from {process.current_state} to {event_name}")


def state_info(process):
    print(f"state of {process.name}:{process.current_state}")


def main():
    RUNNING = 'running'
    WAITING = 'waiting'
    BLOCKED = 'blocked'
    TERMINATED = 'terminated'

    p1, p2 = Process("process1"), Process("process2")
    [state_info(process) for process in (p1, p2)]

    print()
    transition(p1, p1.wait, WAITING)
    transition(p2, p2.terminate, TERMINATED)
    [state_info(p) for p in (p1, p2)]

    print()
    transition(p1, p1.run, RUNNING)
    transition(p2, p2.wait, WAITING)
    [state_info(p) for p in (p1, p2)]

    print()
    transition(p2, p2.run, RUNNING)
    [state_info(p) for p in (p1, p2)]

    print()
    [transition(p, p.block, BLOCKED) for p in (p1, p2)]
    [state_info(p) for p in (p1, p2)]

    print()
    [transition(p, p.terminate, TERMINATED) for p in (p1, p2)]
    [state_info(p) for p in (p1, p2)]


if __name__ == '__main__':
    main()
