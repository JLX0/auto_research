import multiprocessing



def overtime_kill(target_function, target_function_args=None, time_limit=60, ret=True):
    # converting this function into a decorator might make it less convenient

    """
    Run a target function with a time limit and terminate if it exceeds the limit.

    Args:
        target_function (function): The function to be executed.
        target_function_args (tuple or None): Optional arguments to be passed to the target function (default: None).
        time_limit (int): The time limit in seconds (default: 60).
        ret (bool): Flag indicating if some information in the target function needs to be captured (default: True).

    Returns:
        tuple: A tuple containing two elements:
            - A bool indicating whether the execution exceeded the time limit (True) or not (False).
            - A dictionary with the captured information from the target function.

    """

    ret_dict = multiprocessing.Manager().dict()

    if target_function_args is not None:
        p = multiprocessing.Process(target=target_function, args=(ret_dict,) + target_function_args)
    elif ret:
        p = multiprocessing.Process(target=target_function, args=(ret_dict,))
    else:
        p = multiprocessing.Process(target=target_function)

    p.start()
    p.join(time_limit)
    if p.is_alive():
        print(f"The operation takes longer than {time_limit} seconds, terminating the execution...")
        p.terminate()
        p.join()
        return True, dict(ret_dict)
    else:
        print("The operation finishes in time")
        return False, dict(ret_dict)

def retry_overtime_kill(target_function , target_function_args=None , time_limit=60 , maximum_retry=3 , ret=True) :
    """
    Run a target function with a time limit and retry it up to maximum_retry times if it exceeds the limit.

    Args:
        target_function (function): The function to be executed.
        target_function_args (tuple or None): Optional arguments to be passed to the target function (default: None).
        time_limit (int): The time limit in seconds (default: 60).
        maximum_retry (int): The maximum number of retries if the function exceeds the time limit (default: 3).
        ret (bool): Flag indicating if some information in the target function needs to be captured (default: True).

    Returns:
        tuple: A tuple containing two elements:
            - A bool indicating whether the execution was successful (False) or exceeded the retries (True).
            - A dictionary with the captured information from the target function.
    """
    for attempt in range(maximum_retry) :
        print(f"Attempt {attempt + 1} of {maximum_retry}")
        exceeded , result = overtime_kill(target_function , target_function_args , time_limit , ret)

        if not exceeded :
            # Successfully completed within the time limit
            return False , result

        print("Retrying...")

    # If we exhausted all retries
    print("All retries exhausted. The operation failed to complete within the time limit.")
    return True , { }


def retry_overtime_decorator(time_limit=60 , maximum_retry=3 , ret=True) :
    """
    Decorator that retries a function if it exceeds a time limit, with multiprocessing support.

    Args:
        time_limit (int): Maximum seconds allowed per attempt
        maximum_retry (int): Max number of retries if time limit exceeded
        ret (bool): Whether function returns some objects to capture

    Returns:
        Decorator function that wraps target function with retry logic
    """

    def decorator(target_function) :
        def wrapper(*args , **kwargs) :
            # Handle class methods vs regular functions
            if args and hasattr(args[0] , "__class__") :  # Check if first arg is self
                self_instance = args[0]  # Get class instance
                message = args[1]  # Get message arg from method call
                target_function_args = ((message ,) , kwargs)  # Pack args for multiprocessing
                # Lambda to call method with class instance, message and ret_dict
                target_function_with_self = lambda ret_dict , *func_args : target_function(self_instance ,
                                                                                           func_args[0][0] , ret_dict)
            else :
                # For regular functions, pass all args through
                target_function_args = (args , kwargs)
                target_function_with_self = lambda ret_dict , *func_args : target_function(ret_dict , *func_args[0] ,
                                                                                           **func_args[1])

            # Call retry logic with wrapped function
            exceeded , result = retry_overtime_kill(
                target_function=target_function_with_self ,
                target_function_args=target_function_args ,
                time_limit=time_limit ,
                maximum_retry=maximum_retry ,
                ret=ret
                )

            # Return result from shared dict or None if failed
            return result.get('result') if result else None

        return wrapper

    return decorator