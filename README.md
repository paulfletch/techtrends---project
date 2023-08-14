# techtrends---project

TechTrends is an online news sharing app writen in Python.  This project is used to demonstrate practices and tools that can  improve the release and maintenance phases within an application's development lifecycle.

The following activities were undertaken.

* Development of endpoints for accessing metrics and performing healthchecks  Logging was also implemented.
  
* The creation of a Dockerfile to build an image that was initially run in a local container.

* The creation of a GitHub action to automate the packaging of the TechTrends Application  (Continuous Integration).  The GitHub action constructed a new image everytime new commit was made on the main branch.

* The creation of a Kubernetes cluster using K3s, vagrant and VirtualBox.   Using a declarative approach (i.e. by developing YAML manifests), the TechTrends apps was deployed on the cluster.

* The creation of a Helm Chart to allow for the parameterisation of the TechTrend manifests enabling different types of deployment.

* The installtion of a kubernetes controller, ArgoCD.  This was used to sync the Techtrends application deployment to the desired state of a staging and production environment (as confugred by HeLm).  (Continuous Delivery).
