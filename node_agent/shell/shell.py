import logging
import subprocess
import json

logger = logging.getLogger()

# ssh -4 -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 oasis@217.160.36.2
# /home/oasis/mainnet/oasis-core/oasis_core_22.2.7_linux_amd64/oasis-node -a unix:/home/oasis/mainnet/node/data/internal.sock
# check_status = /home/oasis/oasis-node-admin/script/oasis.sh control status


def execute_remote_command_to_json(
    cmd,
    user="oasis",
    ip="127.0.0.1",
):
    logger.info("Command: " + user + "@" + ip + " ".join(cmd))
    out = execute_remote_command_to_string(cmd, user, ip)
    # logger.info("Output: " + out)
    return json.loads(out)


def execute_remote_command_to_string(
    cmd,
    user="oasis",
    ip="127.0.0.1",
):
    result = execute_remote_command(cmd, user, ip)
    # logger.info(
    #     "Result: "
    #     + str(result.returncode)
    #     + " "
    #     + result.stdout
    #     + " "
    #     + result.stderr
    # )
    if result.returncode != 0:
        raise Exception(
            "Error executing remote command: "
            + user
            + "@"
            + ip
            + " "
            + " ".join(cmd)
            + " "
            + result.stderr
        )
    return result.stdout


def execute_remote_command(
    command,
    user="oasis",
    ip="127.0.0.1",
):
    if command is None:
        raise Exception("Command is null")
    cmd = [
        "ssh",
        "-4",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ConnectTimeout=10",
        user + "@" + ip,
    ]
    cmd.extend(command)
    # logger.info("Command: " + " ".join(cmd))
    result = execute_command(cmd)
    return result


def execute_command(cmd):
    if cmd is None:
        raise Exception("Command is null")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    """
    print("Out: \n" + result.stdout + "\n")
    print("Error: \n" + result.stderr + "\n")
    print("Return code: \n" + str(result.returncode) + "\n")
    """
    return result
