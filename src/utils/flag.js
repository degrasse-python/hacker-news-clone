import Rox from 'rox-browser'
import { betaAccess, isLoggedIn, getCompany } from './users'
//import mixpanel from 'mixpanel-browser';
// or with require() syntax:
const Mixpanel = require('mixpanel');

// Enabling the debug mode flag is useful during implementation,
// but it's recommended you remove it for production
const mixpanel = Mixpanel.init('d1396f58aa0a75bbad61e86cc4789c0e'); 


export const Flags = {
  score: new Rox.Flag(false),
  newLink: new Rox.Flag(true), 
  ask: new Rox.Flag(false),
  show: new Rox.Flag(false),
  headerColor: new Rox.Variant('is-dark', ['is-dark', 'is-primary', 'is-white'])
}

export const configurationFetchedHandler = fetcherResults => {
  if (fetcherResults.hasChanges && fetcherResults.fetcherStatus === 'APPLIED_FROM_NETWORK') {
    window.location.reload(false)
  }
}

// EXPERIMENTS ARE DEPRECATED THIS IS USING SDK <5.0
export const impressionHandler = (reporting, experiment) => {
  if (experiment) {
    console.log('flag ' + reporting.name + ' value is ' + reporting.value + ', it is part of ' + experiment.name + ' experiment')
    mixpanel.track('Hacker-News-FM', {
      experiment: experiment.name,
      flag: reporting.name,
      value: reporting.value
    }) 
  } else {
    mixpanel.track('Hacker-News-FM', {
      flag: reporting.name,
      value: reporting.value
    }) 
    console.log('No experiment configured for flag ' + reporting.name + '. default value ' + reporting.value + ' was used')
  }
}

const options = {
  configurationFetchedHandler: configurationFetchedHandler,
  impressionHandler: impressionHandler
}

// Defined Properties
Rox.setCustomBooleanProperty('isBetaUser', betaAccess())
Rox.setCustomBooleanProperty('isLoggedIn', isLoggedIn())
Rox.setCustomStringProperty('company', getCompany())
Rox.setCustomStringProperty('region', getRegion())

Rox.register('default', Flags)
Rox.setup('61117c1f978899d272a714f2', options)



