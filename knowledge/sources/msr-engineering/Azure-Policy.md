# Azure Policy

## What is Azure Policy?
Azure Policy is a service in Azure that you use to create, assign and, manage policies. These policies enforce different rules and effects over your resources, so those resources stay compliant with your corporate standards and service level agreements. Azure Policy meets this need by evaluating your resources for non-compliance with assigned policies.

Policy focuses on resource properties during deployment and for already existing resources. Policy controls properties such as the types or locations of resources.

## Policy Definition



- Require SQL Server 12.0: Validates that all SQL servers use version 12.0. Its effect is to deny all servers that don't meet these criteria.

- Allowed Storage Account SKUs: Determines if a storage account being deployed is within a set of SKU sizes. Its effect is to deny all storage accounts that don't adhere to the set of defined SKU sizes.

- Allowed Resource Type: Defines the resource types that you can deploy. Its effect is to deny all resources that aren't part of this defined list.

- Allowed Locations: Restricts the available locations for new resources. Its effect is used to enforce your geo-compliance requirements.

- Allowed Virtual Machine SKUs: Specifies a set of virtual machine SKUs that you can deploy.

- Apply tag and its default value: Applies a required tag and its default value if it's not specified by the deploy request.

- Enforce tag and its value: Enforces a required tag and its value to a resource.

- Not allowed resource types: Prevents a list of resource types from being deployed.


## Policy Limitations and Issues

1. Policy scope 200 resource count per remediation.
   - ![image.png](/.attachments/image-6ee7058b-eaef-4c2a-bb41-6786602ae64f.png)

2. Resource type issues

   - For example, if you want to deploy a custom script extension, if a custom script extension is already deployed to a VM, the policy remediation will fail because one already exists. Workaround would be to manually remove (either az powershell or cli or via the portal manually), the custom script extension before running the remediation task.

3. Not all ARM functions are supported

   -  Writing a custom policy definition is a pain. A lot of ARM functions are not supported.
Because of this, the reference() function (used by keyvault and some other things) is also not supported. 
We'll likely have creds in code, and that might be exposed to anything the policy is applied to.

4. Guest config feature is still in preview and limited to builtin InSpec/DSC runbooks today.