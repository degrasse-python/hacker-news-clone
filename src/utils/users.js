/* eslint-disable */
// Fake user data
export const userList = [
  {
    username: 'betauser',
    password: 'betauser',
    company: 'acme global',
    region: 'JPN',
    beta_access: true
  },
  {
    username: 'normaluser',
    password: 'normaluser',
    company: 'generic co',
    region: 'USA',
    beta_access: false
  },
  {
    username: 'eurouser',
    password: 'eurouser',
    company: 'USBC',
    region: 'WEURO',
    beta_access: false
  }
]


// Helper functions to pass fake user data
export const betaAccess = () => {
  if (localStorage.getItem('user') === null) {
    return false
  } else {
    let localUser = {}
    userList.map((user) => {
      if (user.username === localStorage.getItem('user')) {
        localUser = user
      }
    })
    return localUser.beta_access
  }
}

export const isLoggedIn = () => {
  return localStorage.getItem('user') !== null
}

export const getCompany = () => {
  if (localStorage.getItem('user') === null) {
    return false
  } else {
    let localUser = {}
    userList.map((user) => {
      if (user.username === localStorage.getItem('user')) {
        localUser = user
      }
    })
    return localUser.company
  }
}

export const getRegion = () => {
  if (localStorage.getItem('user') === null) {
    return false
  } else {
    let localUser = {}
    userList.map((user) => {
      if (user.username === localStorage.getItem('user')) {
        localUser = user
      }
    })
    return localUser.region
  }
}
