import fitz
from fitz import Document
import pandas as pd
from pandas import Series
import os.path as ospath


def load_recepient_names(path: str) -> list[str]:
    names: Series = pd.read_csv(path, dtype=str)["FULL_NAME"]

    names.dropna(inplace=True)
    return list(names)


def assert_validity(page_count: int, chunk_size: int, names: list[str]):
    if page_count % chunk_size != 0:
        print(
            f"WARNING! Page count [{page_count}] is not devisible by chunk size [{chunk_size}]"
        )

    if (page_count // chunk_size) != len(names):
        raise ValueError("Files number and recipients numb/er mismatch")


def split_to_options_recipients(
    joined_pdf_path: str, recipient_names_path: str, output_directory: str
):
    names = load_recepient_names(recipient_names_path)

    src: Document = fitz.open(joined_pdf_path)

    CHUNK_SIZE = 13
    CHUNKS = src.page_count // CHUNK_SIZE

    assert_validity(page_count=src.page_count, chunk_size=CHUNK_SIZE, names=names)

    for chunk_num, recipient_name in zip(range(CHUNKS), names):
        start_page_num = chunk_num * CHUNK_SIZE
        end_page_num = start_page_num + CHUNK_SIZE - 1

        split_file: Document
        with fitz.open() as split_file:
            split_file.insert_pdf(src, from_page=start_page_num, to_page=end_page_num)

            split_file.save(
                ospath.join(
                    output_directory, f"{recipient_name}-options docs 23-04-2023.pdf"
                )
            )


def US_options_recipients():
    split_to_options_recipients(
        joined_pdf_path="data/US/OPTIONS DOCS US.pdf",
        recipient_names_path="data/US/23-04-2023_US MAIL MERGE LIST.csv",
        output_directory="output/US",
    )


def IL_options_recipients():
    split_to_options_recipients(
        joined_pdf_path="data/IL/OPTIONS DOCS IL.pdf",
        recipient_names_path="data/IL/IL102 MAIL MERGE LIST.csv",
        output_directory="output/IL",
    )


def main():
    pass


if __name__ == "__main__":
    main()

    pass
