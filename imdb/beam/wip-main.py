import argparse, csv, io
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.filesystems import FileSystems
from apache_beam.io.filesystem import CompressionTypes
from apache_beam.io.parquetio import WriteToParquet
import pyarrow as pa

# IMDb uses '\N' for null
def to_none(v): 
    return None if v in (r'\N', '', None) else v

# TSV parser: title.basics fields:
# tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres
def parse_line(line):
    parts = line.split('\t')
    return {
        "tconst": parts[0],
        "titleType": to_none(parts[1]),
        "primaryTitle": to_none(parts[2]),
        "originalTitle": to_none(parts[3]),
        "isAdult": 1 if parts[4] == '1' else 0,
        "startYear": int(parts[5]) if parts[5].isdigit() else None,
        "endYear": int(parts[6]) if parts[6].isdigit() else None,
        "runtimeMinutes": int(parts[7]) if parts[7].isdigit() else None,
        "genres": None if parts[8] == r'\N' else parts[8].split(',')
    }

schema = pa.schema([
    pa.field("tconst", pa.string()),
    pa.field("titleType", pa.string()),
    pa.field("primaryTitle", pa.string()),
    pa.field("originalTitle", pa.string()),
    pa.field("isAdult", pa.int8()),
    pa.field("startYear", pa.int32()),
    pa.field("endYear", pa.int32()),
    pa.field("runtimeMinutes", pa.int32()),
    pa.field("genres", pa.list_(pa.string()))
])

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_gcs', required=True, help='gs://.../title.basics.tsv.gz')
    parser.add_argument('--output_prefix', required=True, help='gs://.../curated/title_basics/dt=YYYY-MM-DD/part')
    args, beam_args = parser.parse_known_args(argv)

    opts = PipelineOptions(beam_args, save_main_session=True, streaming=False)

    with beam.Pipeline(options=opts) as p:
        (
            p
            | "ReadTSV" >> beam.io.ReadFromText(args.input_gcs, compression_type=CompressionTypes.AUTO, skip_header_lines=1)
            | "Parse"    >> beam.Map(parse_line)
            | "WriteParquet" >> WriteToParquet(
                    file_path_prefix=args.output_prefix,
                    schema=schema,
                    file_name_suffix=".parquet",
                    num_shards=4
               )
        )

if __name__ == '__main__':
    run()