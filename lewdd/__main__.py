import argparse
import sys
import os
import lewdd

parser = argparse.ArgumentParser(
    prog=sys.executable + " -m lewdd",
    description="Downloads images from popular boards",
    epilog="`domain` must be " + ", ".join(lewdd.domains_to_module)
)
domain_arg = parser.add_argument(
    "domain",
    help="The domain from where download"
)
parser.add_argument(
    "tags", nargs="+",
    help="Tags used to search images"
)
parser.add_argument(
    "-n",
    nargs=1,
    help="Maximun amount of images to download (defaults to infinity)",
    type=int,
    metavar="amount",
    dest="amount"
)
parser.add_argument(
    "-o",
    nargs=1,
    help="Output directory, dafults to `domain tags [tags ...]`",
    metavar="path",
    dest="output"
)


def main(args):
    if args.domain not in lewdd.domains_to_module:
        raise argparse.ArgumentError(domain_arg, parser.epilog)
    if args.output is None:
        output = args.domain + " " + " ".join(args.tags)
    else:
        output = args.output[0]
    if args.amount is not None:
        amount = args.amount[0]
    else:
        amount = None
    os.makedirs(output, exist_ok=True)
    lewdd.domains_to_module[args.domain].download(
        args.tags, output, amount
    )

if __name__ == "__main__":
    main(parser.parse_args())
