import re
from colorama import Fore
import requests
import json
from bs4 import BeautifulSoup



website = 'https://epic7db.com/heroes'
request = requests.get(website)
content = request.text

soup_heroe = BeautifulSoup(content, 'html.parser')

heroe_list= soup_heroe.find('ul', 'hero-list').find_all('li')

link_heroes= []

for links in heroe_list:
    heroes= links.find('a').get('href')
    heroe_name= links.find('div', class_='info').find('h3').get_text(strip=True)
    heroe_links= {
    'name': heroe_name,
    'url': heroes
}
    
    link_heroes.append(heroe_links)




def get_info(link, heroe):

    

    website = link
    request = requests.get(website)
    content = request.text

    # Parsear el HTML
    soup = BeautifulSoup(content, 'html.parser')

    skills= get_skill_info(soup)

    equpiment= get_equipment(soup)
    
    awakens = get_Awakens(soup)

    imprints= get_imprints(soup)

    heroe_info= {
        'heroe': heroe,
        'skills': skills,
        'equipment': equpiment,
        'awakens': awakens,
        'imprints': imprints

    }

    
    # print('return: ',skills, equpiment, awakens, imprints, 'fin del return')
    return heroe_info


    
def get_skill_info(soup):
    skill_data = []

    # Iterar sobre todas las etiquetas encontradas y obtener el texto
    bottom_tags = soup.find('div', class_='skills-list').find_all('div', class_='skill accordion open')
    for index, tag in enumerate(bottom_tags):
        skill_title = tag.find('div', class_='title')
        skill_description = tag.find('div', class_='bottom')
        skill_soulburn = tag.find('div', class_='soulburn')
        skill_cooldown = tag.find('div', class_='cooldown')
        skill_soul_gain = tag.find('div', class_='soul-gain')
        skill_upgrade = tag.find('div', class_='skill-upgrades')

        if skill_title:
            skill_title = skill_title.find('h3').get_text(strip=True)

        if skill_description:
            skill_description = skill_description.find('p').get_text(strip=True)

        if skill_soulburn:
            skill_soulburn = skill_soulburn.find('p').get_text(strip=True)

        if skill_cooldown:
            skill_cooldown = skill_cooldown.get_text(strip=True)

        if skill_soul_gain:
            skill_soul_gain = skill_soul_gain.get_text(strip=True)

        skill_info = {
            'skill_title': skill_title,
            'skill_description': skill_description,
            'skill_soulburn': skill_soulburn,
            'skill_cooldown': skill_cooldown,
            'skill_soul_gain': skill_soul_gain,
            'skill_upgrade': []
        }

        if skill_upgrade:
            # print(f"\n", "\n", "\n", "Skill", index+1, "\n", "\n", "\n")
            upgrades = skill_upgrade.find_all('div', class_='upgrade')
            upgrades_data = []

            for i in upgrades:
                level = i.find('div', 'level').get_text(strip=True)
                description = i.find('div', 'description').get_text(strip=True)
                resources_data = []

                for recursos in i.find_all('div', 'resource'):
                    amount = recursos.find('a').get_text(strip=True)
                    # print(amount)
                    resources_data.append(amount)

                upgrade_data = {
                    'level': level,
                    'description': description,
                    'resources': resources_data
                }

                upgrades_data.append(upgrade_data)  # Agregar cada actualización a la lista de actualizaciones

            skill_info['skill_upgrade'] = upgrades_data  # Asignar la lista de actualizaciones al campo skill_upgrade
        skill_data.append(skill_info)

    return skill_data







def get_equipment(soup):
    equipment_data= []
    #Obtener informacion referente a equipments
    equipment= soup.find('div', class_='equipment')
    if equipment:
        title_equipment= equipment.find('div', class_='title').find('h3').get_text(strip=True)
        stat_equipment= equipment.find('div', class_='details').find('h4').get_text(strip=True)
        stat_value_equpment= equipment.find('div', class_='details').find_all('p')
        min_roll = stat_value_equpment[0].get_text(strip=True)
        max_roll= stat_value_equpment[1].get_text(strip=True)
        # print("\n", "\n", "\n" "Equipment", "\n", "\n", "\n")
        # print(title_equipment, stat_equipment)
        # print(min_roll, max_roll)

        equipment_info= {
            'title_equipment': title_equipment,
            'stat_equipment': stat_equipment,
            'min_roll': min_roll,
            'max_roll': max_roll,
            'equipment_skills': []

        }


        skills_improvements= equipment.find('div', class_='skill-improvements').find_all('div', 'skill')
        if skills_improvements:
            for skills in skills_improvements:
                content= skills.find('div', class_='skill-content')
                title_improvement= content.find('h4').get_text(strip=True)
                description_improvement= content.find('p').get_text(strip=True)
                # print(title_improvement, description_improvement)
                equipment_data.append({'title_improvement': title_improvement, 'description_improvement': description_improvement})


            equipment_info['equipment_skills'] = equipment_data
    
        return equipment_info


def get_Awakens(soup):

    
    resources_awakens= []
    stats_awakens= []
    aweken_skill= None
    awakened_skill= None
    awaken= soup.find('section', id='awakenings')

    if awaken:
        # print("\n", "\n", "\n", "Awakenings", "\n", "\n", "\n")
        
        awakenings= awaken.find('div', class_='section-accordion-content').find_all('div', class_='awakening')
        

    for index , awaken in enumerate(awakenings):
        # print("Awakening", index+1,  "\n", "\n")
        # flex= awaken.find('div', class_='flex')
        stat= awaken.find('div', class_='stats')

        try:
            skill_content= awaken.find_all('div', 'skill-content')
            
        
        except:
            print('skill no encontrada')

         

        #Habilidad despertada
        if skill_content:
            aweken_skill= skill_content[0].find('p').get_text(strip=True)
            awakened_skill= skill_content[1].find('p').get_text(strip=True)
            # print('Awaken skill', aweken_skill, '\n', awakened_skill)


        awaken_data={
            'aweken_skill': aweken_skill,
            'awakened_skill': awakened_skill,
            'stats': [],
            'resource': []
        }  

    
        #Stats ganadas por despertar
        stats= stat.find_all('li')
        stats_list= []
        for s in stats:
            stats_value= s.get_text(strip=True)
            stats_list.append(stats_value)
            # print(stats_value, "\n")

        stats_awakens.append(stats_list)
        
        awaken_data['stats'] = stats_awakens

       
       
       
        cost= awaken.find('div', class_='cost').find_all('div', class_='resource')
        
        resources_list= []
        for resources in cost:
            amount= resources.find('a').get_text(strip=True)
            # print(amount)
            resources_list.append(amount)

        resources_awakens.append(resources_list)
        awaken_data['resource'] = resources_awakens

    return awaken_data







        
def get_imprints(soup):

    imprints_data= []

    print('Imprints')
    imprints_html= soup.find('section', id='memory-imprints')

    if imprints_html:
        imprints= imprints_html.find_all('div', 'memory-imprint')

        li= imprints[0].find_all('li')
        # print('Liberacion')
        imprints_liberacion= []
        for lb in li:
            rank= lb.find('img').get('alt')
            value= lb.get_text(strip=True)
            imprints_liberacion.append({'rank': rank, 'value': value})
            # print(rank, value)

        li= imprints[1].find_all('li')
        # print('Concentacion')
        imprints_concentracion= []
        for c in li:
            rank= c.find('img').get('alt')
            value= c.get_text(strip=True)
            # print(rank, value)
            imprints_concentracion.append({'rank': rank, 'value': value})

        imprints_data.append({'liberation': imprints_liberacion, 'concentration': imprints_concentracion})

    return imprints_data




for a in link_heroes:
    # print(a['name'])
    heroes= get_info(a['url'], a['name'])
    print(heroes)

















# website = 'https://epic7db.com/heroes/abigail'
# request = requests.get(website)
# content = request.text


# # Parsear el HTML
# soup = BeautifulSoup(content, 'html.parser')

# bottom_tags = soup.find('div', class_='skills-list').find_all('div', class_='skill accordion open')



# # Iterar sobre todas las etiquetas encontradas y obtener el texto
# for index, tag in enumerate(bottom_tags):
#     skill_title = tag.find('div', class_='title')
#     skill_description = tag.find('div', class_='bottom')
#     skill_soulburn = tag.find('div', class_='soulburn')
#     skill_cooldown = tag.find('div', class_='cooldown')
#     skill_soul_gain = tag.find('div', class_='soul-gain')
#     skill_upgrade = tag.find('div', class_='skill-upgrades')

#     if skill_title:
#        skill_title= skill_title.find('h3').get_text(strip=True)

#     if skill_description:
#         skill_description= skill_description.find('p').get_text(strip=True)

#     if skill_soulburn:
#         skill_soulburn= skill_soulburn.find('p').get_text(strip=True)

#     if skill_cooldown:
#         skill_cooldown= skill_cooldown.get_text(strip=True)

#     if skill_soul_gain:
#         skill_soul_gain= skill_soul_gain.get_text(strip=True)
    
    
    
    
#     if skill_upgrade:
#         print(f"\n", "\n", "\n", "Skill", index+1, "\n", "\n", "\n")
#         upgrades= skill_upgrade.find_all('div', class_='upgrade')
        
#         for i in upgrades:
#             level= i.find('div', 'level').get_text(strip=True)
#             description= i.find('div', 'description').get_text(strip=True)
#             cost= i.find('div', 'cost').get_text(strip=True)
#             print(level, description)
#             resources= i.find_all('div', 'resource')
#             for recursos in resources:
#                 amount= recursos.find('a').get_text(strip=True)
#                 print(amount)
            


#     print("\n", skill_title, ":  " , skill_description, skill_soulburn, skill_cooldown, skill_soul_gain)


# #Obtener informacion referente a equipments
# equipment= soup.find('div', class_='equipment')
# if equipment:
#     title_equipment= equipment.find('div', class_='title').find('h3').get_text(strip=True)
#     stat_equipment= equipment.find('div', class_='details').find('h4').get_text(strip=True)
#     stat_value_equpment= equipment.find('div', class_='details').find_all('p')
#     min_roll = stat_value_equpment[0].get_text(strip=True)
#     max_roll= stat_value_equpment[1].get_text(strip=True)
#     print("\n", "\n", "\n" "Equipment", "\n", "\n", "\n")
#     print(title_equipment, stat_equipment)
#     print(min_roll, max_roll)

#     skills_improvements= equipment.find('div', class_='skill-improvements').find_all('div', 'skill')
#     if skills_improvements:
#         for skills in skills_improvements:
#             content= skills.find('div', class_='skill-content')
#             title_improvement= content.find('h4').get_text(strip=True)
#             description_improvement= content.find('p').get_text(strip=True)
#             print(title_improvement, description_improvement)




# awaken= soup.find('section', id='awakenings')

# if awaken:
#     print("\n", "\n", "\n", "Awakenings", "\n", "\n", "\n")
    
#     awakenings= awaken.find('div', class_='section-accordion-content').find_all('div', class_='awakening')
    

# for index , awaken in enumerate(awakenings):
#     print("Awakening", index+1,  "\n", "\n")
#     # flex= awaken.find('div', class_='flex')
#     stat= awaken.find('div', class_='stats')

#     try:
#         skill_content= awaken.find_all('div', 'skill-content')
        
    
#     except:
#         print('skill no encontrada')
        
#     #Habilidad despertada
#     if skill_content:
#         aweken_skill= skill_content[0].find('p').get_text(strip=True)
#         awakened_skill= skill_content[1].find('p').get_text(strip=True)
#         print('Awaken skill', aweken_skill, '\n', awakened_skill)
    
   
#     #Stats ganadas por despertar
#     stats= stat.find_all('li')
#     for s in stats:
#         stats_value= s.get_text(strip=True)
#         print(stats_value, "\n")

#     cost= awaken.find('div', class_='cost').find_all('div', class_='resource')
    

#     for resources in cost:
#         amount= resources.find('a').get_text(strip=True)
#         print(amount)
    
    

# print('Imprints')
# imprints_html= soup.find('section', id='memory-imprints')

# if imprints_html:
#     imprints= imprints_html.find_all('div', 'memory-imprint')

#     li= imprints[0].find_all('li')
#     print('Liberacion')
#     for lb in li:
#         rank= lb.find('img').get('alt')
#         value= lb.get_text(strip=True)
#         print(rank, value)

#     li= imprints[1].find_all('li')
#     print('Concentacion')
#     for c in li:
#         rank= c.find('img').get('alt')
#         value= c.get_text(strip=True)
#         print(rank, value)

   