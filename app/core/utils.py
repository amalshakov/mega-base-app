def sort_users_by_uploads(users: list[dict[str, int]]):
    n = len(users)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (
                users[j]["number_upload_files"] < users[j + 1]["number_upload_files"] or
                (
                    users[j]["number_upload_files"] == users[j + 1]["number_upload_files"] and
                    users[j]["username"] > users[j + 1]["username"]
                )
            ):
                users[j], users[j + 1] = users[j + 1], users[j]
    return users


def sort_users_by_uploads2(users: list[dict[str, int]]):
    return sorted(users, key=lambda x: x["number_upload_files"], reverse=True)
