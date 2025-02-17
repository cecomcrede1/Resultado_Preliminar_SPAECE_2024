import pandas as pd
import os

def analyze_spaece_data(file_path, output_folder='output'):
    """
    Analyzes SPAECE data from a CSV or Excel file and outputs all results to a single Excel sheet,
    including results for each Componente Curricular and Etapa.

    Args:
        file_path (str): Path to the CSV or Excel file.
        output_folder (str): Path to the folder where the output Excel file will be saved.
                             Defaults to 'output' folder in the script's directory.
    """

    try:
        # Read the data from the CSV or Excel file
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            print("Error: Unsupported file format. Please provide a CSV or Excel file.")
            return

        # Check if required columns exist
        required_columns = ['ESCOLA', 'ETAPA', 'COMPONENTE CURRICULAR', 'TURMA', 'ESTUDANTE', 'AVALIADO', 'PROFICIENCIA MÉDIA', 'FAIXAS']
        for col in required_columns:
            if col not in df.columns:
                print(f"Error: Required column '{col}' not found in the file.")
                return

        # Data Cleaning and Preparation
        df['PROFICIENCIA MÉDIA'] = pd.to_numeric(df['PROFICIENCIA MÉDIA'], errors='coerce')  # Convert to numeric, handle errors
        df['AVALIADO'] = df['AVALIADO'].str.upper()  # Standardize 'AVALIADO' column
        df['FAIXAS'] = df['FAIXAS'].astype(str)  # Ensure 'FAIXAS' is string type
        df['AVALIADO'] = df['AVALIADO'].replace('-', 'NÃO')  # Replace '-' with 'NÃO'

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Prepare to store results
        all_results = []
        output_file = os.path.join(output_folder, 'spaece_results.xlsx')

        # Iterate over Componentes Curriculares and Etapas
        for componente in df['COMPONENTE CURRICULAR'].unique():
            componente_df = df[df['COMPONENTE CURRICULAR'] == componente]

            for etapa in df['ETAPA'].unique():
                etapa_df = componente_df[componente_df['ETAPA'] == etapa]

                # Calculations
                total_students_evaluated = etapa_df[etapa_df['AVALIADO'] == 'SIM'].shape[0]
                total_students = etapa_df.shape[0]
                average_proficiency = etapa_df['PROFICIENCIA MÉDIA'].mean()
                num_schools = etapa_df['ESCOLA'].nunique()  # Count unique schools

                # FAIXAS distribution
                faixa_counts = etapa_df['FAIXAS'].value_counts().to_dict()

                # Store results
                results = {
                    'Componente Curricular': componente,
                    'Etapa': etapa,
                    'Number of Schools': num_schools,
                    'Average Proficiency': average_proficiency,
                    'Total Students Evaluated': total_students_evaluated,
                    'Total Students': total_students
                }

                # Include FAIXAS distribution and percentages
                all_faixas = df['FAIXAS'].unique()
                for faixa in all_faixas:
                    count = faixa_counts.get(faixa, 0)
                    results[f'Total {faixa}'] = count
                    percentage = (count / total_students_evaluated) * 100 if total_students_evaluated > 0 else 0
                    results[f'Percentage {faixa}'] = percentage

                all_results.append(results)

        # Convert to DataFrame and save to sheet
        results_df = pd.DataFrame(all_results)
        results_df.to_excel(output_file, sheet_name='All Results', index=False)

        print(f"Results saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = r'C:\Users\Dell\Downloads\SPAECE_preliminar_2024\Coleta de Dados SPAECE 2024\RESULTADO SPAECE NOMINAL_spaece_2024.xlsx'
analyze_spaece_data(file_path)
