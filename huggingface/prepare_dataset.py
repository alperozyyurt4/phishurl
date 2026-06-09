#!/usr/bin/env python3
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Convert the extracted PhishURL CSV into train/validation/test Parquet files for Hugging Face."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the extracted features CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        default="hf_dataset",
        help="Output directory for Parquet split files.",
    )
    parser.add_argument(
        "--label-column",
        default="label",
        help="Target label column used for stratified splitting.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.10,
        help="Fraction of rows used for test split.",
    )
    parser.add_argument(
        "--validation-size",
        type=float,
        default=0.10,
        help="Fraction of rows used for validation split.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible splits.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    import pandas as pd
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(input_path)
    if args.label_column not in df.columns:
        raise ValueError(
            f"Label column '{args.label_column}' was not found. Available columns: {list(df.columns)}"
        )

    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=df[args.label_column],
    )

    validation_fraction_of_train = args.validation_size / (1.0 - args.test_size)
    train_df, validation_df = train_test_split(
        train_df,
        test_size=validation_fraction_of_train,
        random_state=args.seed,
        stratify=train_df[args.label_column],
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    train_df.to_parquet(output_dir / "train.parquet", index=False)
    validation_df.to_parquet(output_dir / "validation.parquet", index=False)
    test_df.to_parquet(output_dir / "test.parquet", index=False)

    print(f"Input rows: {len(df):,}")
    print(f"Train rows: {len(train_df):,}")
    print(f"Validation rows: {len(validation_df):,}")
    print(f"Test rows: {len(test_df):,}")
    print(f"Output directory: {output_dir.resolve()}")
    print("Label distribution:")
    for split_name, split_df in (
        ("train", train_df),
        ("validation", validation_df),
        ("test", test_df),
    ):
        counts = split_df[args.label_column].value_counts(normalize=True).sort_index()
        formatted = ", ".join(f"{label}: {ratio:.4f}" for label, ratio in counts.items())
        print(f"  {split_name}: {formatted}")


if __name__ == "__main__":
    main()
