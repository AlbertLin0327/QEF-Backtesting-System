### Import necessary library ###
import argparse
import shutil
import os
import json
import csv


def save_result(manager: object, path: str, args: argparse.Namespace) -> None:
    """
    Handle the final result image and print strategy performance

    Parameters
    ----------
    manager: object
        The class "PortfolioManager" used in Backtesting
    path: str
        The base file path to store result
    args: argparse.Namespace
        The arguments used in backtesting

    Returns
    -------
    None
    """

    # Create base directory
    os.mkdir(path)

    # Plot result and save to images
    image_path = path + "/images"
    os.mkdir(image_path)

    manager.plot_all(image_path)

    # Save arguements to args.txt
    arg_path = path + "/args.txt"
    with open(arg_path, "w") as f:
        json.dump(args.__dict__, f, indent=2)

    # Copy strategy and saved to result directory
    strategy_path = "Sandbox/Strategy/" + args.strategy_file + ".py"
    saved_strategy_path = path + "/" + args.strategy_file + ".py"

    shutil.copy(
        strategy_path,
        saved_strategy_path,
    )

    # Print necessay ratio and save to csv
    print(
        f"--- Result of Strategy {args.strategy_file} on Universe {args.universe_file} ---"
    )
    print(f"sharpe ratio = {manager.cal_sharpe_ratio()}")
    print(f"total return ratio = {manager.cal_total_return()}")
    print(f"annual sharpe ratio = {manager.cal_annual_sharpe_ratio()}")
    print(f"annual return ratio = {manager.cal_annual_return()}")
    print(
        f"--- End Backtesting and result store to history_strategy {args.save_file} ---"
    )

    ratio_path = path + "/ratio.csv"

    with open(ratio_path, "w") as f:
        writer = csv.writer(f)

        # Write rowname
        writer.writerow(
            [
                "sharpe ratio",
                "total return ratio",
                "annual sharpe ratio",
                "annual return ratio",
            ]
        )

        # Write numeric data
        writer.writerow(
            [
                manager.cal_sharpe_ratio(),
                manager.cal_total_return(),
                manager.annual_sharpe_ratio,
                manager.annual_return,
            ]
        )
