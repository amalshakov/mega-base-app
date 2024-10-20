def sort_users_by_uploads(users: list[dict[str, int]]):
    return sorted(users, key=lambda x: x["number_upload_files"], reverse=True)
