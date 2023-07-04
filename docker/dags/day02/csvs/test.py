import pandas as pd
table_list_df = pd.read_csv( filepath_or_buffer='tablist.csv',
                                sep=',',
                                quotechar='"'
                            )
table_list = table_list_df['tablename'].to_list()

print(table_list)