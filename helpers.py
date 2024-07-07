def get_api_key(file_path):
    try:
        with open(file_path, "r") as file:
            return file.readline().strip()

    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"
