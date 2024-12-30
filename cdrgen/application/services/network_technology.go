package application

import "project/domain"

type SaveEntitiesUseCase struct {
	Repository domain.EntityRepository
}

func (uc *SaveEntitiesUseCase) Execute(entities []domain.Entity) error {
	for _, entity := range entities {
		if err := uc.Repository.Save(entity); err != nil {
			return err
		}
	}
	return nil
}