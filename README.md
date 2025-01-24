# Home Assitant Intergration for energyLIVE API

## About 

This custom compenent for [Home Assistant](https://www.home-assistant.io) provides integration with [energyLIVE](https://www.smartenergy.at/energylive).

## Installation

### HACS

1. Ensure that [HACS](https://hacs.xyz) is installed.

2. Open HACS, then select `Integrations`.

3. Select &#8942; and then `Custom repositories`.

4. Set `Repository` to *https://github.com/berwinter/ha_energylive*  
   and `Category` to _Integration_.

5. Install **energyLIVE** integration via HACS:

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=berwinter&repository=ha_energylive)

   If the button doesn't work: Open `HACS` > `Integrations` > `Explore & Download Repositories` and select integration `energyLIVE`.

### Manual

1. Copy the folder `custom_components/energylive` to `custom_components` in your Home Assistant `config` folder.

## Configure

1. Obtain energyLIVE API key via smartENERGY app or webpage:
![Obtain API key for energyLIVE](./doc/obtain_api_key.png)

2. Add energyLIVE custom integration in Home Assistant and provide your API key:
![Add energyLIVE integration](./doc/add_integration.png)

3. Your energyLIVE devices (interface and gateway) will be added in Home Assistant and it starts logging:
![Interace and gateway devices](./doc/devices.png)

