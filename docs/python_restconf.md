# RESTCONF with Python

Demonstration of utilizing the Python `requests` module to configure network devices using RESTCONF.

This repository is intended to be used in the [Programmability Foundations Lab](https://www.wwt.com/lab/programmability-foundations-lab) but you can modify the inventory and variables to work with any topology.

This lab uses several different yang models including:
- `ietf-interface.yang` model for configuration of the interfaces
- `Cisco-IOS-XE-ospf.yang` for configuration of the OSPF process
- `Cisco-IOS-XE-ospf-oper.yang` for validation of the OSPF configuration

## Prep Steps

While you can use any environment to run this demo, the path of least resistance is to use the [Programmability Foundations Lab](https://www.wwt.com/lab/programmability-foundations-lab).  This lab will have all of the necessary Python libraries, development tools and the network that matches the inventory file.

Follow these steps to utilize the [Programmability Foundations Lab](https://www.wwt.com/lab/programmability-foundations-lab):

1. Reserve the [Programmability Foundations Lab](https://www.wwt.com/lab/programmability-foundations-lab)

2. Connect to your newly launched lab

3. Run the **yang-explorer** container [optional]

   We will not be diving into the yang-explorer in any great depth but you could launch this to inspect the models.

    ```
    docker run --name yang-explorer -p 8088:8088 -d dmfigol/yang-explorer
    ```

4. Start container
    ```shell
    docker container run -itv ~/development:/development wwt01/alpine-network-dev
    ```

5. Clone the repository (from within the container you launched)
`git clone https://github.com:wwt/restconf_python_demo.git`

6. `cd' into the cloned repository

## Walk Through

![topology](_images/net_topology_simple.png)

Our goal is simple...add a loopback interface to each router, then configure OSPF between the two.

1. Review the existing router configs
   Q: Is there a loopback0 interface?
   Q: Is OSPF configured on the device?
2. Enabling RESTCONF
   Q: Is `restconf` enabled on the device?
   A: Yes

   Q: Is `http secure-server` enabled on the device?
   A: Yes

   Q: Is there a privilege 15 user created?
   A: Yes
3. Visual Studio Code and Containers