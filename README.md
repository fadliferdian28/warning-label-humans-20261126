# Warning Label for Humans: One Line, Big Laugh

A single-line warning label, entered into the make.fun bundle competition. The joke
is the whole product: a unit that volunteers for moving day, brings exactly one tote
bag, and walks off with the scissors you actually liked.

## Live badges

[![make.fun competition](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)

[![make.fun rank](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/fadliferdian28/warning-label-humans-20261126/rank.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)

[![make.fun reward](https://make.fun/badge/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85/fadliferdian28/warning-label-humans-20261126/reward.svg)](https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85)

Bounty page: <https://make.fun/bounty/u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85>

## The entry

`entry.txt` is frozen. It is 112 bytes, hashes to
`149cc69b76863fb2e38890da1b88ce7295820734845d39c3760e7c7dd346b883`, and consists of
one line of 112 characters. Nothing in this repo rewrites it; the script only copies
it.

## What the script does

`main.py` is a small stdlib-only courier:

1. Reads `entry.txt` from the directory that holds the script.
2. Checks the byte length against the pinned `112` and the SHA-256 against the
   pinned digest.
3. Re-runs the competition gate: valid UTF-8, one line only, not whitespace, and
   1–160 characters.
4. Refuses to continue if the destination resolves to the source file itself.
5. Atomically writes the untouched bytes to `$MAKEFUN_OUTPUT_DIR/entry.txt`, or to
   `/output/entry.txt` when that variable is not set.

Any failed check prints a reason to stderr and exits non-zero; success prints one
short line and exits `0`.

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Join in

New to make.fun? Sign up with referral code `effxtzzc`:
<https://make.fun/?ref=effxtzzc>

## License

See `LICENSE`.
