<template>
  
  <b-navbar :type="headerColor" id="nav">
    <template slot="brand">
      <b-navbar-item href="/">
        <strong>HN</strong>
      </b-navbar-item>
      <b-navbar-item v-if="isBeta">
        <i>Beta tester</i>
      </b-navbar-item>
      <b-navbar-item v-if="isDev">
        <span @click="rolloutOverride">DEV</span>
      </b-navbar-item>
    </template>
    <template slot="start">
      <b-navbar-item href="/">
        Hot
      </b-navbar-item>
      <b-navbar-item id="ask" v-if="ask" href="/ask">
        Ask
      </b-navbar-item>
      <b-navbar-item id="show" v-if="show" href="/show">
        Show
      </b-navbar-item>
    </template>
    <template slot="end">
      <b-navbar-item tag="div">
        <div class="buttons">
          <a class="button is-black" v-if="loggedIn" @click="logout">
            Log out
          </a>
          <a class="button is-black" v-else href="/login">
            Log in
          </a>
        </div>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<style lang="stylus">

#nav {
  margin-bottom: 15px
}
</style>

<script>
/* eslint-disable */
import Rox from 'rox-browser'
import { Flags } from '../utils/flag'
import { mapState, mapActions } from 'vuex'
import { betaAccess, getRegion, getCompany } from '../utils/users'
// const Mixpanel = require('mixpanel')
// const mixpanel = Mixpanel.init('d1396f58aa0a75bbad61e86cc4789c0e')

// call mixpanel sdk
/* A/B Testing
platform.track_links(
  // payload
  '#ask', 'Feature - Ask Click', 
  {
      'clicks': 1
      ,ask: Flags.ask.isEnabled() 
  });

mixpanel.track_links(
  '#show', 'Feature - Show Click', 
  // payload
  {
    'clicks': 1
    ,show: Flags.show.isEnabled() // place a flag call in this payload
  });
*/

export default {
  
  track () {
    analytics.identify(' {{user.id}} ', {
      name: '{{user.username}}',
      company: '{{user.company}}'
      })
    analytics.page('Home', {
      headerColor: Flags.headerColor.getValue(),
      ask: Flags.ask.isEnabled(),
      show: Flags.show.isEnabled(),
      isBeta: betaAccess()
    })
  },
  
  data () {
    return {
      // isDev: process.env.NODE_ENV === 'development',
      isDev: process.env.NODE_ENV === 'production',      
      headerColor: Flags.headerColor.getValue(),
      ask: Flags.ask.isEnabled(),
      show: Flags.show.isEnabled(),
      isBeta: betaAccess(),
      getRegion: getRegion(),
      getCompany: getCompany()
    }
  },

  methods: {
    rolloutOverride: () => {
      Rox.showOverrides()
    },
    ...mapActions([
      'logout'
    ])
  },
  computed: mapState([
    'loggedIn'
  ])
}
</script>
