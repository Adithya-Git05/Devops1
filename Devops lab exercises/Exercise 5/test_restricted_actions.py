import docker

IMAGE = "flask-apparmor"
PROFILE = "my-apparmor-profile"


def main() -> None:
    client = docker.from_env()
    container = client.containers.run(
        IMAGE,
        security_opt=[f"apparmor={PROFILE}"],
        detach=True,
    )

    try:
        python_check = container.exec_run(["python", "-c", "pass"])
        if python_check.exit_code != 0:
            raise RuntimeError(
                "The container's Python runtime did not start: "
                f"{python_check.output.decode(errors='replace')}"
            )

        read_check = container.exec_run(
            [
                "python",
                "-c",
                "from pathlib import Path; Path('/etc/passwd').read_text()",
            ]
        )
        read_output = read_check.output.decode(errors="replace")
        if read_check.exit_code == 0 or "permission denied" not in read_output.lower():
            raise AssertionError(
                "AppArmor did not deny reading /etc/passwd: "
                f"exit={read_check.exit_code}, output={read_output!r}"
            )
        print(f"/etc/passwd read denied (exit {read_check.exit_code})")
        print(read_output.strip())

        binary_check = container.exec_run(["/bin/bash", "-c", "exit 0"])
        binary_output = binary_check.output.decode(errors="replace")
        if binary_check.exit_code == 0:
            raise AssertionError("AppArmor allowed execution of /bin/bash")
        print(f"/bin/bash execution denied (exit {binary_check.exit_code})")
        if binary_output:
            print(binary_output.strip())
    finally:
        container.stop()
        container.remove()


if __name__ == "__main__":
    main()
