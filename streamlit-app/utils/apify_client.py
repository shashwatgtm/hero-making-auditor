from apify_client import ApifyClient as BaseApifyClient
import time

class ApifyClient:
    def __init__(self, token):
        self.client = BaseApifyClient(token)
        
    def run_customer_discovery(self, input_data):
        """Run the hero customer discovery actor"""
        actor_id = "your-username/hero-customer-discovery"
        
        try:
            run = self.client.actor(actor_id).call(run_input=input_data)
            
            # Wait for completion
            while run["status"] in ["RUNNING", "READY"]:
                time.sleep(5)
                run = self.client.run(run["id"]).get()
            
            if run["status"] == "SUCCEEDED":
                # Get dataset items
                dataset_id = run["defaultDatasetId"]
                items = self.client.dataset(dataset_id).list_items()
                return items.items[0] if items.items else None
            else:
                raise Exception(f"Actor run failed with status: {run['status']}")
                
        except Exception as e:
            raise Exception(f"Failed to run actor: {str(e)}")