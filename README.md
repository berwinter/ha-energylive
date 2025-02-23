# Home Assistant Integration for energyLIVE API

## About 

This custom compenent for [Home Assistant](https://www.home-assistant.io) provides integration with [energyLIVE](https://www.smartenergy.at/energylive). energyLIVE provideds realtime data from your smartmeter. This integration requires an API key, which can be generated from the smartENERGY App or website. Currently reading live data from gateway and interface devices are supported. The following sensors will be automatically added for those devices:

![Gateway sensors](./doc/enties_gateway.png)

![Interface sensors](./doc/enties_interface.png)

## Installation

### HACS

1. Ensure that [HACS](https://hacs.xyz) is installed.

2. Open HACS, then select `Integrations`.

3. Select &#8942; and then `Custom repositories`.

4. Set `Repository` to *https://github.com/berwinter/ha-energylive*  
   and `Category` to _Integration_.

5. Install **energyLIVE** integration via HACS:

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=berwinter&repository=ha-energylive)

   If the button doesn't work: Open `HACS` > `Integrations` > `Explore & Download Repositories` and select integration `energyLIVE`.
   ![Install energyLIVE](./doc/install.png)


### Manual

1. Copy the folder `custom_components/energylive` to `custom_components` in your Home Assistant `config` folder.

## Configure

1. Obtain energyLIVE API key via smartENERGY app or webpage:
   ![Obtain API key for energyLIVE](./doc/obtain_api_key.png)

3. Add energyLIVE custom integration in Home Assistant and provide your API key:
   ![Add energyLIVE integration](./doc/add_integration.png)

4. Your energyLIVE devices (interface and gateway) will be added in Home Assistant and it starts logging:
   ![Interace and gateway devices](./doc/devices.png)

