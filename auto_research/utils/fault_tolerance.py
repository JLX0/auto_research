from __future__ import annotations

import multiprocessing
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

# Type variables for generic function types
T = TypeVar("T")
R = TypeVar("R")


def overtime_kill(
        target_function: Callable[... , Any] ,
        target_function_args: tuple | None = None ,
        time_limit: int = 60 ,
        ret: bool = True ,
        ) -> tuple[bool , dict] :
    """Run a target function with a time limit and terminate if it exceeds the limit.

    Args:
        target_function:
            The function to be executed.
        target_function_args:
            Optional arguments to be passed to the target function.
        time_limit:
            The time limit in seconds.
        ret:
            Flag indicating if some information in the target function needs to be captured.

    Returns:
        A tuple containing:
            - A bool indicating whether the execution exceeded the time limit (True) or not (False).
            - A dictionary with the captured information from the target function.

    Example:
        .. testcode::

            import time


            def long_running_task(ret_dict):
                # Simulate heavy computation
                time.sleep(5)
                ret_dict["result"] = 42


            # Function will complete since time_limit > sleep duration
            exceeded, result = overtime_kill(long_running_task, time_limit=10)
            if not exceeded:
                print(f"Task completed with result: {result['result']}")  # Outputs: 42

            # Function will be terminated since time_limit < sleep duration
            exceeded, result = overtime_kill(long_running_task, time_limit=3)
            if exceeded:
                print("Task was terminated due to timeout")
    """
    ret_dict = multiprocessing.Manager().dict()

    if target_function_args is not None :
        p = multiprocessing.Process(
            target=target_function ,
            args=(ret_dict ,) + target_function_args ,
            )
    elif ret :
        p = multiprocessing.Process(target=target_function , args=(ret_dict ,))
    else :
        p = multiprocessing.Process(target=target_function)

    p.start()
    p.join(time_limit)

    if p.is_alive() :
        print(
            f"The operation takes longer than {time_limit} seconds, "
            "terminating the execution..."
            )
        p.terminate()
        p.join()
        return True , dict(ret_dict)

    print("The operation finishes in time")
    return False , dict(ret_dict)


def retry_overtime_kill(
        target_function: Callable[... , Any] ,
        target_function_args: tuple | None = None ,
        time_limit: int = 60 ,
        maximum_retry: int = 3 ,
        ret: bool = True ,
        ) -> tuple[bool , dict] :
    """Run a target function with a time limit and retry it up to maximum_retry times if it exceeds the limit.

    Args:
        target_function:
            The function to be executed.
        target_function_args:
            Optional arguments to be passed to the target function.
        time_limit:
            The time limit in seconds.
        maximum_retry:
            The maximum number of retries if the function exceeds the time limit.
        ret:
            Flag indicating if some information in the target function needs to be captured.

    Returns:
        A tuple containing:
            - A bool indicating whether the execution was successful (False) or exceeded the retries (True).
            - A dictionary with the captured information from the target function.

    Example:
        .. testcode::

            import time


            def unstable_task(ret_dict):
                # Simulate an unstable computation that sometimes takes longer
                sleep_time = 8 if time.time() % 2 == 0 else 3
                time.sleep(sleep_time)
                ret_dict["result"] = 42


            # Function might succeed on retry if timing works out
            exceeded, result = retry_overtime_kill(unstable_task, time_limit=5, maximum_retry=3)
            if not exceeded:
                print(f"Task completed with result: {result['result']}")
            else:
                print("Task failed after all retries")
    """
    for attempt in range(maximum_retry) :
        print(f"Attempt {attempt + 1} of {maximum_retry}")
        exceeded , result = overtime_kill(target_function , target_function_args , time_limit ,
                                          ret)

        if not exceeded :
            # Successfully completed within the time limit
            return False , result

        print("Retrying...")

    # If we exhausted all retries
    print("All retries exhausted. The operation failed to complete within the time limit.")
    return True , { }


def retry_overtime_decorator(
        time_limit: int = 60 ,
        maximum_retry: int = 3 ,
        ret: bool = True ,
        ) -> Callable[[Callable[... , R]] , Callable[... , Optional[R]]] :
    """Decorator that retries a function if it exceeds a time limit, with multiprocessing support.

    This decorator wraps a function to provide retry functionality when the function execution
    exceeds a specified time limit. It supports both regular functions and class methods.

    Args:
        time_limit:
            Maximum seconds allowed per attempt.
        maximum_retry:
            Max number of retries if time limit exceeded.
        ret:
            Whether function returns some objects to capture.

    Returns:
        A decorator function that wraps the target function with retry logic.

    Example:
        .. testcode::

            import time


            @retry_overtime_decorator(time_limit=5, maximum_retry=3)
            def long_computation(ret_dict):
                # Simulate a computation that takes varying time
                sleep_time = 7 if time.time() % 3 == 0 else 4
                time.sleep(sleep_time)
                ret_dict["result"] = 42


            # Will retry up to 3 times if sleep_time is 7
            result = long_computation()
            if result is not None:
                print(f"Computation completed: {result}")


            # Example with a class method
            class TimeConsumingTask:
                @retry_overtime_decorator(time_limit=4, maximum_retry=2)
                def process_data(self, data, ret_dict):
                    time.sleep(3)  # Simulate processing
                    ret_dict["result"] = len(data)


            task = TimeConsumingTask()
            result = task.process_data("sample data")
            if result is not None:
                print(f"Processed data length: {result}")
    """

    def decorator(target_function: Callable[... , R]) -> Callable[... , Optional[R]] :
        def wrapper(*args: Any , **kwargs: Any) -> Optional[R] :
            # Handle class methods vs regular functions
            if args and hasattr(args[0] , "__class__") :  # Check if first arg is self
                self_instance = args[0]  # Get class instance
                message = args[1]  # Get message arg from method call
                target_function_args = ((message ,) , kwargs)  # Pack args for multiprocessing

                def target_function_with_self(ret_dict , *func_args) :
                    return target_function(self_instance , func_args[0][0] , ret_dict)

            else :
                # For regular functions, pass all args through
                target_function_args = (args , kwargs)

                def target_function_with_self(ret_dict , *func_args) :
                    return target_function(ret_dict , *func_args[0] , **func_args[1])

            # Call retry logic with wrapped function
            exceeded , result = retry_overtime_kill(
                target_function=target_function_with_self ,
                target_function_args=target_function_args ,
                time_limit=time_limit ,
                maximum_retry=maximum_retry ,
                ret=ret ,
                )

            # Return result from shared dict or None if failed
            return result.get("result") if result else None

        return wrapper

    return decorator
