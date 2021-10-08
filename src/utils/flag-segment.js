import Rox from 'rox-browser'
import { betaAccess, isLoggedIn, getCompany } from './users'
import Analytics from '@segment/analytics.js-core/build/analytics'
import SegmentIntegration from '@segment/analytics.js-integration-segmentio'

// Segment
const analytics = new Analytics()

// add Segment's own integration ( or any other device mode integration ) 
analytics.use(SegmentIntegration)

// define the integration settings object. 
// Since we are using only Segment integration in this example, we only have 
// "Segment.io" in the integrationSettings object
const integrationSettings = {
  'Segment.io': {
    apiKey: 'xJ64dheGnIeusujfFNQwNYQnkXcHEKuU',
    retryQueue: true,
    addBundledMetadata: true
  }
}
// init segment.io
analytics.initialize(integrationSettings)

// Happy tracking! 
// analytics.track('');

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
    analytics.page('Hacker-News-Demo', {
      experiment: experiment.name,
      flag: reporting.name,
      value: reporting.value
    }) 
  } else {
    analytics.page('Hacker-News-Demo', {
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

Rox.register('default', Flags)
Rox.setup('61117c1f978899d272a714f2', options)



