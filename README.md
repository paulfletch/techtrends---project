# techtrends---project

TechTrends is a simple online news sharing platform.  This project demonstrated practices and tools to improve the application lifecycle throughout the release and maintenance phases.

The following tasks were undertaken.

* Development endpoints for metrics and healthcheck and implement logging.
  
* Create a Dockerfile and build an image.  This was run in a local container.

* Create a GitHub action to automate the packaging of the TechTrends Application  (Continuous Integration).  The GitHub action constructs a new image every new commit on the main branch.

* A Kubernetes cluster was created on K3s using vagrant and VirtualBox.   Using a declarative approach (i.e. developing YAML manifests), the TechTrends apps was deployed.

* Through the creation of help chards, a template configuration manager (Helm) was used to parameterise TechTrend manifests.

*  ArgoCD was used to release the Techtrends application to a staging and production environments using the templated manifests from the Helm chart.  That is, an automated and templated procedure to deploy TechTends to multiple environments (Continuous Delivery).
