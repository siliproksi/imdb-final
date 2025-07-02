import { getCountryLabel, getCityLabel } from '../data/countries'

export default {
  methods: {
    getLocalizedCountry(countryKey) {
      if (!countryKey) return countryKey
      if (countryKey === 'All') {
        return this.$t('search.all')
      }
      return getCountryLabel(countryKey, this.$i18n.locale)
    },
    
    getLocalizedCity(countryKey, cityKey) {
      if (!cityKey) return cityKey
      return getCityLabel(countryKey, cityKey, this.$i18n.locale)
    }
  }
}