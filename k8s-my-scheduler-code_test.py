# _*_ coding: utf-8 _*_

import requests
import time
import json

SCHEDULER_NAME = "songjinquan"
API_SERVER = "http://10.128.0.118:8080"
API_URL = {
    "pods": "/api/v1/pods",
    "nodes": "/api/v1/nodes",
    "binding": "/api/v1/namespaces/{0}/pods/{1}/binding"
}


def get_pods(url):
    pods = requests.get(url)
    pods_list = list()
    if pods.status_code == 200:
        # print(pods.json()["items"])
        pods_list = [
            {
                "name": x["metadata"]["name"],
                "namespace": x["metadata"]["namespace"]
            } for x in pods.json()["items"] if x["status"]["phase"] == "Pending" and x["metadata"]["annotations"]["scheduler.alpha.kubernetes.io/name"] == SCHEDULER_NAME
        ]
    return pods_list


def get_nodes(url):
    nodes = requests.get(url)
    nodes_list = list()
    if nodes.status_code == 200:
        nodes_list = [x["metadata"]["name"] for x in nodes.json()["items"]]

    return nodes_list


def chose_node(nodes):
    '''scheduler'''
    chosen = None
    for node in nodes:
        if node.endswith("118"):  # �����ã�ֻ��ѡ����ip��179��β�Ľڵ�
            chosen = node
            break
    return chosen


def main():
    pods_list = get_pods(API_SERVER + API_URL["pods"])
    nodes_list = get_nodes(API_SERVER + API_URL["nodes"])
    if pods_list == []:
        print("There is no pod need to be scheduled.")
        return True

    for pod in pods_list:
        chosen = chose_node(nodes_list)
        if chosen == None:
            print("There is no node be chosen.")
            return True

        data = {"apiVersion": "v1",
                "kind": "Binding",
                "metadata": {"name": pod["name"]},
                "target": {"apiVersion": "v1", "kind": "Node", "name": chosen}
                }
        bind = API_SERVER + \
               API_URL["binding"].format(pod["namespace"], pod["name"])
        headers = {"Content-type": "application/json",
                   "Accept": "application/json"}
        r = requests.post(bind, data=json.dumps(data), headers=headers)
        if r.status_code == 201:
            print("Assigned {0} to {1}.".format(pod["name"], chosen))
        else:
            print(r.text)
    time.sleep(3)


if __name__ == "__main__":

    while True:
        time.sleep(1)
        main()
