import shutil
import os
import json


def save_result(manager, path: str, args):

    image_path = path + "/images"
    os.mkdir(image_path)
    manager.plot_all(image_path)

    with open(path + "/args.txt", "w") as f:
        json.dump(args.__dict__, f, indent=2)

    shutil.copy(
        "Sandbox/Strategy/" + args.strategy_file + ".py",
        path + "/" + args.strategy_file + ".py",
    )

    print(f"sharpe ratio={manager.cal_sharpe_ratio()}")
