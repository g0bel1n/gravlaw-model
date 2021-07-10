from gravLawModel import GravLawModel

if __name__ == "__main__":
    model = GravLawModel(country="France", iso_a3="FRA")
    print("Computing...")
    model.flow_calculate()
    print("End of computing")
    model.save()
    print("png saved")
