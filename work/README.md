* work

app/csv_db_loader
- controllers
- presenters
- interfaces


infra/
- models
    - provider
    - region
    - service
    - period
- loggers
- adapters
    - provider_repo
    - region_repo
    - service_repo
    - period_repo

interactor
- dto
- interfaces
- usecases
    - provider_usecase
    - region_usecase
    - service_usecase
    - period_usecase
    - init_usecase
- validations
- errors

domain