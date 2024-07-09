def get_api_key(file_path):
    """
    Retrieves the API key from a specified file.

    Parameters:
    file_path (str): The path to the file containing the API key.

    Returns:
    str: The API key as a string if the file is found and read successfully.
         Returns "File not found" if the file does not exist.
         Returns an error message if another exception occurs.
    """
    
    try:
        with open(file_path, "r") as file:
            return file.readline().strip()

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"


def is_world_server_valid(world: str) -> bool:
    """
    Checks if the provided server region name is valid.

    Parameters:
    world (str): The server region name to validate.

    Returns:
    bool: True if the server region name is valid, False otherwise.
          Prints an error message if the server region name is invalid.
    """
    
    if world not in ["america", "asia", "europe", "sea"]:
        print(f"Error: Server region name {world} is invalid. Return null")
        return False
    else: 
        return True
