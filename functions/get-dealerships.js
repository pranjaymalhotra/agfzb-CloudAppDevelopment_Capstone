const axios = require('axios');

async function get(url, config) {
    try {
        const response = await axios.get(url, config)
        return {
            status: response.status,
            data: response.data
        }
    } catch (error) {
        return {
            status: error.response.status,
            data: error.response.body
        }
    }
}
 
async function main(params) {
    const auth = {
        username: params.cloudant_user,
        password: params.cloudant_password
    }
    const config = {
        auth: auth
    }
    
    if (typeof(params.state) == 'undefined') {
        state = ''
    } else {
        state = params.state
    }
    
    state = state.split('"').join('')
    
    if (state == '') {
        //If no param state, get all of states
        url = params.cloudant_url + '/dealerships/_design/api/_view/all?include_docs=True'
    }
    else {
        //Else get dealerships for state
        url = params.cloudant_url + '/dealerships/_design/api/_view/by-st?include_docs=True&key='
        url = url + '%22' + state + '%22'
    }
    payload = await get(url, config)
     
    //If error, return error
    if (payload.status != 200) {
         return {
            headers: { 'Content-Type': 'application/json' },
            statusCode: payload.status,
            body: 500
        }
    }
     
    if (payload.data.rows.length <= 0) {
         return {
            headers: { 'Content-Type': 'application/json' },
            statusCode: 404,
            body: {}
        }
     }
     
    dealerships = []
     
    payload.data.rows.forEach(row => dealerships.push({
         id: row.doc.id,
         city: row.doc.city,
         state: row.doc.state,
         st: row.doc.st,
         address: row.doc.address,
         zip: row.doc.zip,
         lat: row.doc.lat,
         long: row.doc.long
    }))
      
    return {
        headers: { 'Content-Type': 'application/json' },
        statusCode: 200,
        body: dealerships
    }
}
