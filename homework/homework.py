"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import zipfile
import os

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    
    os.makedirs('files/output', exist_ok=True)
    
    all_data = []
    
    # Leer todos los archivos zip
    for i in range(10):
        zip_path = f'files/input/bank-marketing-campaing-{i}.csv.zip'
        
        with zipfile.ZipFile(zip_path, 'r') as z:
            csv_name = z.namelist()[0]
            
            with z.open(csv_name) as f:
                df = pd.read_csv(f)
                all_data.append(df)
    
    # Combinar todos los datos
    data = pd.concat(all_data, ignore_index=True)
    
    # Crear client.csv
    client = data[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    
    # Limpiar job
    client['job'] = client['job'].str.replace('.', '').str.replace('-', '_')
    
    # Limpiar education
    client['education'] = client['education'].str.replace('.', '_')
    client['education'] = client['education'].replace('unknown', pd.NA)
    
    # Convertir credit_default
    client['credit_default'] = (client['credit_default'] == 'yes').astype(int)
    
    # Convertir mortgage (mantener nombre original)
    client['mortgage'] = (client['mortgage'] == 'yes').astype(int)
    
    client.to_csv('files/output/client.csv', index=False)
    
    # Crear campaign.csv (mantener nombre original de la columna)
    campaign = data[['client_id', 'number_contacts', 'contact_duration', 
                    'previous_campaign_contacts', 'previous_outcome', 
                    'campaign_outcome', 'day', 'month']].copy()
    
    # Convertir previous_outcome
    campaign['previous_outcome'] = (campaign['previous_outcome'] == 'success').astype(int)
    
    # Convertir campaign_outcome
    campaign['campaign_outcome'] = (campaign['campaign_outcome'] == 'yes').astype(int)
    
    # Crear last_contact_date
    months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
              'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    
    campaign['last_contact_date'] = '2022-' + campaign['month'].map(months) + '-' + campaign['day'].astype(str).str.zfill(2)
    campaign = campaign.drop(['day', 'month'], axis=1)
    
    campaign.to_csv('files/output/campaign.csv', index=False)
    
    # Crear economics.csv (mantener nombre original)
    economics = data[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    
    economics.to_csv('files/output/economics.csv', index=False)


if __name__ == "__main__":
    clean_campaign_data()