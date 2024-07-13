from processor.processor.filter import Filter
from processor.processor.processor import Processor
from processor.serializer.serializer import Serializer
from processor.transformer.transformer import TransformerFactory


def process_csv(
    csv_data: str, selected_columns: str, row_filter_definitions: str
) -> None:
    """
    Process the CSV data by applying filters and selecting columns.

    @param csv The CSV data to be processed.
    @param selectedColumns The columns to be selected from the CSV data.
    @param rowFilterDefinitions The filters to be applied to the CSV data.

    @return void
    """
    csv_transformer = TransformerFactory.create_csv_transformer(line_delimiter=",")

    transformed_lazy_data_DTO = csv_transformer.data_transform_lazy(csv_data)

    csv_filter = Filter(row_filter_definitions, transformed_lazy_data_DTO.headers)

    processed_lazy_data_DTO = Processor(transformed_lazy_data_DTO, csv_filter)

    serialized_data = Serializer(processed_lazy_data_DTO.build_lazy()).stringify(
        selected_columns
    )

    print(serialized_data)


def process_csv_file(
    csv_file_path: str, selected_columns: str, row_filter_definitions: str
) -> None:
    """
    Process the CSV file by applying filters and selecting columns.

    @param csvFilePath The path to the CSV file to be processed.
    @param selectedColumns The columns to be selected from the CSV data.
    @param rowFilterDefinitions The filters to be applied to the CSV data.

    @return void
    """
    try:
        with open(csv_file_path, "r") as file:
            csv_transformer = TransformerFactory.create_csv_transformer(
                line_delimiter=","
            )
            transformed_lazy_data_DTO = csv_transformer.file_transform_lazy(file)

            csv_filter = Filter(
                row_filter_definitions, transformed_lazy_data_DTO.headers
            )
            processed_lazy_data_DTO = Processor(transformed_lazy_data_DTO, csv_filter)

            serialized_data = Serializer(
                processed_lazy_data_DTO.build_lazy()
            ).stringify(selected_columns)

            print(serialized_data)
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
