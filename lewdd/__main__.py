import argparse
import sys
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
    help="Amount of images to download (defaults to as much as posible)",
    type=int,
    metavar="amount",
    dest="amount"
)
parser.add_argument(
    "-o",
    nargs=1,
    help="Output directory",
    metavar="path",
    dest="output"
)


def main(args):
    if args.domain not in lewdd.domains_to_module:
        raise argparse.ArgumentError(domain_arg, parser.epilog)
    if args.output is None:
        output = args.domain + " ".join(args.tags)
    else:
        output = args.output
    lewdd.domains_to_module[args.domain].download(
        args.tags, output, args.amount
    )

if __name__ == "__main__":
    main(parser.parse_args())
