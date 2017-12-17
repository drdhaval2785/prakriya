# version

v0.0.1 - Baby steps
Date - 15 October 2017

## Usage

1. api.sanskritworld.in/v0.0.1/verbform/verb
2. api.sanskritworld.in/v0.0.1/verbform/meaning
3. api.sanskritworld.in/v0.0.1/verbform/gana
4. api.sanskritworld.in/v0.0.1/verbform/number
5. api.sanskritworld.in/v0.0.1/verbform/madhaviya
6. api.sanskritworld.in/v0.0.1/verbform/kshiratarangini
7. api.sanskritworld.in/v0.0.1/verbform/dhatupradipa
8. api.sanskritworld.in/v0.0.1/verbform/uohyd
9. api.sanskritworld.in/v0.0.1/verbform/jnu
10. api.sanskritworld.in/v0.0.1/verbform/verbslp
11. api.sanskritworld.in/v0.0.1/verbform/lakara
12. api.sanskritworld.in/v0.0.1/verbform/upasarga
13. api.sanskritworld.in/v0.0.1/verbform/padadecider_id
14. api.sanskritworld.in/v0.0.1/verbform/padadecider_sutra
15. api.sanskritworld.in/v0.0.1/verbform/it_sutra
16. api.sanskritworld.in/v0.0.1/verbform/it_id
17. api.sanskritworld.in/v0.0.1/verbform/it_status
18. api.sanskritworld.in/v0.0.1/verbform/derivation
19. api.sanskritworld.in/v0.0.1/verbform/prakriya
20. api.sanskritworld.in/v0.0.1/verbform/prakriya/machine
21. api.sanskritworld.in/v0.0.1/verbform


# v0.0.2

1. Generated files on ubuntu system. Windows is case insensitive.
Therefore earlier acIkarat and acIkaRat went into the same file.
See https://github.com/drdhaval2785/prakriya/issues/1
2. Prevented overwriting of data. See https://github.com/drdhaval2785/prakriya/issues/2.
3. In case of 404 errors, user is prompted the correct URI structure. See https://github.com/drdhaval2785/prakriya/issues/3.
4. Hosted API on api.sanskritworld.in. See https://github.com/drdhaval2785/prakriya/issues/5.
5. Changed webservice from flask to flask-restplus. See https://github.com/drdhaval2785/prakriya/issues/6.
6. Documented API via swagger, builtin in flask-restplus. See https://github.com/drdhaval2785/prakriya/issues/6#issuecomment-352167563.
7. Documented implementation details in swagger i.e. docstrings in methods.
See https://github.com/drdhaval2785/prakriya/issues/7
8. Return form info along with prakriyA.
See https://github.com/drdhaval2785/prakriya/issues/10
9. Enable input and output transliterations in API. See https://github.com/drdhaval2785/prakriya/issues/9
10. Corrected a typo in ASIrliN forms. See https://github.com/drdhaval2785/prakriya/issues/11
11. Corrected error in candrabindu of SLP1. See https://github.com/drdhaval2785/prakriya/issues/12
12. Started giving sUtra text for derivation in all APIs having prakriya in them. See https://github.com/drdhaval2785/prakriya/issues/13
13. Kept the intermediate and final forms as comma separated values instead of a list. See https://github.com/drdhaval2785/prakriya/issues/14
