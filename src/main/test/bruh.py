from dns import resolver as dr

new_dr = dr.Resolver()
new_dr.nameservers = ['8.8.4.4']
print(new_dr.resolve('abc.com'))
