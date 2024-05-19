#!/bin/bash

full=$(curl "$1" 2>/dev/null)

idp=$(echo "$full" | sed -e 's/.*IDPSSODescriptor[^>]*>\(.*\)<\/IDPSSODescriptor.*/\1/')

almost_target=$(echo "$idp" | sed -e 's/.*<SingleLogoutService\([^>]*\)>.*/\1/')
target=$(echo "$almost_target" | sed -e 's/.*Location="\(.*\)".*/\1/')

cert_string=$(echo "$idp" | sed -e 's/.*X509Certificate[^>]*>\(.*\)<\/X509Certificate.*/\1/')
cert_pem=$(echo $cert_string | fold -w64)
cert_pem=$(
echo -----BEGIN CERTIFICATE-----
echo "${cert_pem}"
echo -----END CERTIFICATE-----)

almost_finger=$(openssl x509 -noout -fingerprint -in <(echo "${cert_pem}"))
finger=$(echo "$almost_finger" | sed -e 's/.*=//')


echo "  ## Saml plugin configuration"
echo "  DISCOURSE_SAML_TITLE: \"Pega SAML\""
echo "  DISCOURSE_SAML_NAME_IDENTIFIER_FORMAT: \"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress\""
echo "  DISCOURSE_SAML_TARGET_URL: ${target}"
echo "  DISCOURSE_SAML_CERT_FINGERPRINT: \"${finger}\""
echo "  DISCOURSE_SAML_REQUEST_METHOD: post"
echo "  DISCOURSE_SAML_FULL_SCREEN_LOGIN: true"
echo "  DISCOURSE_SAML_CERT: \"${cert_pem}\""