import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_country_summary_image(summary_data: dict, output_file="summary.png"):
    folder_path = "cache/"
    output_path = os.path.join(folder_path, output_file)

    # Create the folder (and any parent folders) if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    total_countries = summary_data.get("total_countries", 0)
    top_5 = summary_data.get("top_5", [])
    last_refresh = summary_data.get("last_refreshed_at")

    # --- Prepare chart data ---
    names = [row["name"] for row in top_5]
    gdps = [row["estimated_gdp"] for row in top_5]

    # --- Create figure ---
    plt.figure(figsize=(9, 6))
    plt.suptitle("Country Data Summary", fontsize=16, fontweight="bold")

    # Total count & timestamp
    plt.text(
        0.02, 0.9,
        f"Total Countries: {total_countries:,}",
        fontsize=13, fontweight="bold",
        transform=plt.gcf().transFigure,
    )

    ts_text = last_refresh if last_refresh else "No data"
    plt.text(
        0.02, 0.84,
        f"Last Refresh: {ts_text}",
        fontsize=11,
        transform=plt.gcf().transFigure,
    )

    # GDP bar chart
    plt.barh(names[::-1], gdps[::-1], color="skyblue")
    plt.xlabel("Estimated GDP (in billions)")
    plt.ylabel("Country")
    plt.title("Top 5 Countries by Estimated GDP", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.8])

    # Save image
    plt.savefig(output_path)
    plt.close()
    print(f"Summary image saved to {output_path}")
