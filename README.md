# LoxBerry-Plugin-myenergi

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url]

This Plugin gets every 1 minutes the actual power values and sends them to the miniserver via udp messages. Current power is negative when power to the grid is injected and positive when power from the grid is consumed. The value is then ready to use with the loxone energy manager.

Supposed to work on LoxBerry > v2.2, tested on LoxBerry v3.0

Plugin information and documentation page can be found at:
https://wiki.loxberry.de/plugins/myenergi_bridge/start

<!-- GETTING STARTED -->
## Getting Started

### Function of the plugin
The plugin triggers a cronjob script every 1min that reads various data from the myenergi api, adapts the values to kW and then sends them via UDP to the miniserver, using an indented and space-padded json format to permit for easy value extraction on the miniserver side. Grid values will be negative for exported energy and positive for imported energy. These values will be useful in the miniserver for various components, such as the energy manager.

The plugin is basically a clone and adaption of  the [LoxBerry-Plugin-solaredge](https://github.com/ingenarius/LoxBerry-Plugin-solaredge) which was a perfect starting point to jot down this plugin in the shortest time possible. 

### Installation
The installation should be straight forward via web interface of the loxberry.

### Configuration options
The only settings are:

* API Key
* Serial
* Miniserver UDP Port

## Data sent via JSON to miniserver
The following is an example of a json struct sent to the miniserver, containing the following data:

* date
* time
* home consumption power in kW
* grid import or export in kW
* solar generation in kW
* charger power in kW
* battery power in kW
* voltage in Volt * 10
* frequency
* daily imported energy in kWh
* daily exported energy in kWh
* daily generated energy in kWh
* daily green energy in kWh

```
{
"dat": "05-03-2023" ,
"tim": "09:10:03" ,
"con": 1.03 ,
"grd": -1.55 ,
"gen": 2.58 ,
"chg": 0.0 ,
"bat": 0.0 ,
"vol": 2354 ,
"frq": 50 ,
"eimp": 6.49 ,
"eexp": 0.25 ,
"egen": 4.57 ,
"egrn": 0.0
}
```

## Setup in the Loxone Config Software
* Create a "Virtual UDP Input"
* Create one or more "Virtual UDP Input Commands" to parse the relevant values for your application

### Example reading six values
![image](https://user-images.githubusercontent.com/62471240/222951606-849e57b9-7843-4cd4-b73a-5755e39bfff3.png)

### Setup of virtual udp input
![image](https://user-images.githubusercontent.com/62471240/222951626-5619c068-fd2e-4f77-a742-5bcf4ea433b1.png)

### Setup of virtual udp input command
![image](https://user-images.githubusercontent.com/62471240/222951715-46ca21e3-36a1-4bd0-97c3-6dde6df30426.png)

<!-- LICENSE -->
## License

Distributed under the Apache License 2.0. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Christoph Moar - [@christophmoar](https://twitter.com/christophmoar) 

Project Link: [https://github.com/christophmoar/LoxBerry-Plugin-myenergi](https://github.com/christophmoar/LoxBerry-Plugin-myenergi)

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This complete plugin framework has been cloned from Loxberry-Plugin-solaredge by ingenarius, thanks for the template.
The plugin itself and its usage would not be possible without these fine projects:

* [LoxBerry-Plugin-solaredge](https://github.com/ingenarius/LoxBerry-Plugin-solaredge)
* [Loxberry](https://wiki.loxberry.de)
* [Loxforum](https://www.loxforum.com)


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/christophmoar/LoxBerry-Plugin-myenergi.svg?style=for-the-badge
[contributors-url]: https://github.com/christophmoar/LoxBerry-Plugin-myenergi/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/christophmoar/LoxBerry-Plugin-myenergi.svg?style=for-the-badge
[forks-url]: https://github.com/christophmoar/LoxBerry-Plugin-myenergi/network/members
[stars-shield]: https://img.shields.io/github/stars/christophmoar/LoxBerry-Plugin-myenergi.svg?style=for-the-badge
[stars-url]: https://github.com/christophmoar/LoxBerry-Plugin-myenergi/stargazers
[issues-shield]: https://img.shields.io/github/issues/christophmoar/LoxBerry-Plugin-myenergi.svg?style=for-the-badge
[issues-url]: https://github.com/christophmoar/LoxBerry-Plugin-myenergi/issues
[license-shield]: https://img.shields.io/github/license/christophmoar/LoxBerry-Plugin-myenergi.svg?style=for-the-badge
[license-url]: https://github.com/christophmoar/LoxBerry-Plugin-myenergi/blob/main/LICENSE


