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




PS /home/mohamed> Get-AzResource | Format-Table

Name                                        ResourceGroupName                                               ResourceType                                     Location
----                                        -----------------                                               ------------                                     --------
NetworkWatcher_canadaeast                   NetworkWatcherRG                                                Microsoft.Network/networkWatchers                canadaeast
ASP-biopportunitedevrg-8987                 bi-opportunite-dev-rg                                           Microsoft.Web/serverFarms                        eastus
biopportunitedevrgb03e                      bi-opportunite-dev-rg                                           Microsoft.Storage/storageAccounts                eastus
biopportunitedevrga55b                      bi-opportunite-dev-rg                                           Microsoft.Storage/storageAccounts                eastus
bfinop                                      bi-opportunite-dev-rg                                           Microsoft.Batch/batchAccounts                    canadaeast
biopportunitedevrg8bba                      bi-opportunite-dev-rg                                           Microsoft.Storage/storageAccounts                eastus
ASP-biopportunitedevrg-91cc                 bi-opportunite-dev-rg                                           Microsoft.Web/serverFarms                        eastus
test1998678678567                           bi-opportunite-dev-rg                                           Microsoft.Web/sites                              eastus
ASP-biopportunitedevrg-8b6d                 bi-opportunite-dev-rg                                           Microsoft.Web/serverFarms                        canadaeast
datalakeopportunitedev                      bi-opportunite-dev-rg                                           Microsoft.Storage/storageAccounts                canadaeast
espacetravailsynapsedev/SQL_OPPORTUNITE_DEV bi-opportunite-dev-rg                                           Microsoft.Synapse/workspaces/sqlPools            canadaeast
espacetravailsynapsedev                     bi-opportunite-dev-rg                                           Microsoft.Synapse/workspaces                     canadaeast
finops-mi                                   bi-opportunite-dev-rg                                           Microsoft.ManagedIdentity/userAssignedIdentities canadaeast
mom_databr                                  bi-opportunite-dev-rg                                           Microsoft.Databricks/workspaces                  canadaeast
unity-catalog-access-connector              databricks-rg-mom_databr-kucxfjqfuxola                          Microsoft.Databricks/accessConnectors            canadaeast
workers-sg                                  databricks-rg-mom_databr-kucxfjqfuxola                          Microsoft.Network/networkSecurityGroups          canadaeast
dbmanagedidentity                           databricks-rg-mom_databr-kucxfjqfuxola                          Microsoft.ManagedIdentity/userAssignedIdentities canadaeast
workers-vnet                                databricks-rg-mom_databr-kucxfjqfuxola                          Microsoft.Network/virtualNetworks                canadaeast
dbstoragennrxilcd4tuna                      databricks-rg-mom_databr-kucxfjqfuxola                          Microsoft.Storage/storageAccounts                canadaeast
espacetravailsynapsedev/SQL_OPPORTUNITE_DEV synapseworkspace-managedrg-c94de7d9-87bb-4a1f-a50f-c28969f240f9 Microsoft.Sql/servers/databases                  canadaeast
espacetravailsynapsedev                     synapseworkspace-managedrg-c94de7d9-87bb-4a1f-a50f-c28969f240f9 Microsoft.Sql/servers                            canadaeast
espacetravailsynapsedev/master              synapseworkspace-managedrg-c94de7d9-87bb-4a1f-a50f-c28969f240f9 Microsoft.Sql/servers/databases                  canadaeast
finops-keyvault1                            bi-opportunite-dev-rg                                           Microsoft.KeyVault/vaults                        eastus
finops-workspace                            bi-opportunite-dev-rg                                           Microsoft.Synapse/workspaces                     canadaeast
finops-workspace                            synapseworkspace-managedrg-b5b007c9-84ae-493a-a573-6f33e8ca5999 Microsoft.Sql/servers                            canadaeast
finops-workspace/master                     synapseworkspace-managedrg-b5b007c9-84ae-493a-a573-6f33e8ca5999 Microsoft.Sql/servers/databases                  canadaeast

PS /home/mohamed> Get-AzResource -Name finops-keyvault1 | Format-List

Name              : finops-keyvault1
ResourceGroupName : bi-opportunite-dev-rg
ResourceType      : Microsoft.KeyVault/vaults
Location          : eastus
ResourceId        : /subscriptions/1ebabb15-8364-4ada-8de3-a26abeb7ad59/resourceGroups/bi-opportunite-dev-rg/providers/Microsoft.KeyVault/vaults/finops-keyvault1
Tags              : 
                    Name    Value 
                    ======  ======
                    projet  finops
                    
                    
                    
resource allocation
- allocation rule 
- priority / 