import Rox from 'rox-browser'
import { betaAccess, isLoggedIn, getCompany } from './users'

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
    analytics.page('Home', {
      experiment: experiment.name,
      flag: reporting.name,
      value: reporting.value
    }) 
  } else {
    console.log('No experiment configured for flag ' + reporting.name + '. default value ' + reporting.value + ' was used')
  }
}

const options = {
  configurationFetchedHandler: configurationFetchedHandler,
  impressionHandler: impressionHandler
}

// Property
Rox.setCustomBooleanProperty('isBetaUser', betaAccess())
Rox.setCustomBooleanProperty('isLoggedIn', isLoggedIn())
Rox.setCustomStringProperty('company', getCompany())

Rox.register('default', Flags)
Rox.setup('61117c2efca8decf560ff100', options)
