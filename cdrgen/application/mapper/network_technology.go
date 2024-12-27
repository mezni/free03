package mapper

func MapToPerson(dto  NetworkTechnologyDTO, id int) Person {
    return  {
        ID:   id
        Name: dto.Name,
        Description :  dto.Description,
    }
}
