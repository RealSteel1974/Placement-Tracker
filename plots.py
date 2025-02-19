import matplotlib.pyplot as plt
from database import Session
from models import PlacementData


session = Session()

def create_dashboard_plots():
    # Query data
    results = session.query(PlacementData).all()
    batches = [record.Batch for record in results]
    dac = [record.DAC for record in results]

    dbda = [record.DBDA for record in results] if hasattr(results[0], 'DBDA') else [0] * len(batches)
    total_students = [record.TotalStudents for record in results] if hasattr(results[0], 'TotalStudents') else dac


    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 2x2 grid
    fig.suptitle('Placement Data Dashboard')

    # Line Chart
    axs[0, 0].plot(batches, dbda, marker='o')
    axs[0, 0].set_title('DBDA Placements Over Batches ')
    axs[0, 0].set_xlabel('Batch')
    axs[0, 0].set_ylabel('DBDA Placement Percentage')
    axs[0, 0].tick_params(axis='x', rotation=45)

    # Bar Chart
    axs[0, 1].bar(batches, dbda)
    axs[0, 1].set_title('Bar Chart of DBDA Placements ')
    axs[0, 1].set_xlabel('Batch')
    axs[0, 1].set_ylabel('DBDA Placement Percentage')
    axs[0, 1].tick_params(axis='x', rotation=45)


    # Box Plot
    axs[1, 0].boxplot([dac, dbda], labels=['DAC', 'DBDA'])
    axs[1, 0].set_title('Distribution of DAC and DBDA Placements')
    axs[1, 0].set_ylabel('Placement Percentage')

    # Stacked Bar Chart
    axs[1, 1].bar(batches, dac, color='skyblue', label='DAC')
    axs[1, 1].bar(batches, dbda, bottom=dac, color='lightcoral', label='DBDA')
    axs[1, 1].set_title('Stacked Bar Chart of DAC and DBDA Placements')
    axs[1, 1].set_xlabel('Batch')
    axs[1, 1].set_ylabel('Placement Percentage')
    axs[1, 1].tick_params(axis='x', rotation=45)
    axs[1, 1].legend()

    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for the suptitle

    # Save the combined plot
    plt.savefig('static/dashboard_plot.png')
    plt.close()

