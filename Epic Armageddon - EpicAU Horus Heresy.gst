<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem id="5924-e3fb-5543-3044" name="Epic Armageddon - EpicAU Horus Heresy" revision="10" battleScribeVersion="2.03" authorName="EpicAU Horus Heresy (community) - BSData conversion" authorContact="" authorUrl="https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page" xmlns="http://www.battlescribe.net/schema/gameSystemSchema">
  <readme>Horus Heresy supplement for Net Epic Armageddon developed by the EpicAU community. Converted from the archived EpicAU wiki (https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page). Rules text is summarised; see the wiki and the NetEA rulebook for full wording. Add a primary army force, then optionally an Allied Contingent force from another catalogue.</readme>
  <publications>
    <publication id="e750-7f22-5501-6b8d" name="EpicAU Wiki - Horus Heresy Supplement" publisherUrl="https://web.archive.org/web/20201111221247/http://epicau.com/mw/index.php/Main_Page"/>
  </publications>
  <costTypes>
    <costType id="points" name="pts" defaultCostLimit="-1.0" hidden="false"/>
    <costType id="f52a-9ea6-2bb3-2a37" name="Transport space" defaultCostLimit="-1.0" hidden="true"/>
    <costType id="9b58-ba34-d974-341c" name="Transport units" defaultCostLimit="-1.0" hidden="true"/>
    <costType id="53ea-b6c5-c500-fb0e" name="Assault Claw space" defaultCostLimit="-1.0" hidden="true"/>
  </costTypes>
  <profileTypes>
    <profileType id="5e39-4dae-2d39-3e75" name="Unit">
      <characteristicTypes>
        <characteristicType id="c497-e948-9495-63cc" name="Type"/>
        <characteristicType id="6644-be7b-6187-e2cd" name="Speed"/>
        <characteristicType id="462a-a0d1-1868-59af" name="Armour"/>
        <characteristicType id="cc43-f6de-2798-fb59" name="CC"/>
        <characteristicType id="5376-4e08-3028-9ae5" name="FF"/>
        <characteristicType id="4e39-030c-4e18-12e0" name="Weapons"/>
        <characteristicType id="eac3-6a94-cb92-4e59" name="Range"/>
        <characteristicType id="d5dc-a6b1-1fdc-bb30" name="Firepower"/>
        <characteristicType id="9000-985e-2684-f643" name="Weapon Notes"/>
        <characteristicType id="072f-7f4a-18eb-925e" name="Notes"/>
      </characteristicTypes>
    </profileType>
    <profileType id="a3a4-6088-7144-07b6" name="War Engine">
      <characteristicTypes>
        <characteristicType id="060e-c5b1-5155-b844" name="Type"/>
        <characteristicType id="f5e6-b542-20ce-5e5f" name="Speed"/>
        <characteristicType id="4dec-9e47-21ab-b418" name="Armour"/>
        <characteristicType id="720d-edd1-f5f0-6a73" name="CC"/>
        <characteristicType id="6aea-f6b7-e754-4fea" name="FF"/>
        <characteristicType id="8053-23b9-7271-666e" name="Weapons"/>
        <characteristicType id="3069-85d5-1a17-f28e" name="Range"/>
        <characteristicType id="8397-b72d-83b9-ce5f" name="Firepower"/>
        <characteristicType id="a2db-1347-a5a5-688a" name="Weapon Notes"/>
        <characteristicType id="b1b3-f018-48be-a953" name="Notes"/>
        <characteristicType id="4829-b112-1d5a-a2af" name="Damage Capacity"/>
        <characteristicType id="008c-819b-8cb1-5aad" name="Void Shields"/>
        <characteristicType id="1acb-7796-a6da-6469" name="Critical Hit"/>
      </characteristicTypes>
    </profileType>
    <profileType id="34e7-5c9b-31e6-d0ce" name="Weapon">
      <characteristicTypes>
        <characteristicType id="4b89-f4f0-2a22-1135" name="Range"/>
        <characteristicType id="75e3-c2c3-88a9-45ff" name="Firepower"/>
        <characteristicType id="b5b6-fc7a-ca09-528c" name="Notes"/>
      </characteristicTypes>
    </profileType>
  </profileTypes>
  <categoryEntries>
    <categoryEntry id="71ca-c9e1-da76-27e2" name="Line Detachment" hidden="false"/>
    <categoryEntry id="287c-ab86-2eee-2e9f" name="Support Detachment" hidden="false"/>
    <categoryEntry id="a748-07af-1c49-b4e9" name="Lord of War" hidden="false"/>
    <categoryEntry id="4c9b-9993-547d-98ef" name="Daemonic Horde" hidden="false"/>
    <categoryEntry id="1a88-1c24-d20b-5666" name="Greater Daemon Horde" hidden="false"/>
    <categoryEntry id="7b9d-f4a2-bc1c-dc74" name="Followers of Chaos" hidden="false"/>
    <categoryEntry id="797e-7656-6bf5-482c" name="Special Selection" hidden="false"/>
    <categoryEntry id="b980-0dfd-c54d-3593" name="Allies &amp; Lords of War" hidden="false"/>
    <categoryEntry id="2012-97f3-e7fc-26b6" name="Supreme Commander" hidden="false"/>
    <categoryEntry id="5568-d0c7-8d10-dce0" name="Spacecraft" hidden="false"/>
    <categoryEntry id="ef4e-f5b8-029c-6e3f" name="Primarch" hidden="false"/>
    <categoryEntry id="5485-21a2-ac74-b69e" name="Character" hidden="false"/>
    <categoryEntry id="ba14-d0f1-f942-df54" name="Configuration" hidden="false"/>
    <categoryEntry id="dca3-6748-53f0-e4bb" name="Tactical Transport Space" hidden="true"/>
    <categoryEntry id="1c1a-168c-d3cf-3310" name="Upgraded Unit" hidden="true"/>
    <categoryEntry id="592b-0da0-9d99-08ca" name="Not available with the chosen Configuration" hidden="false"/>
    <categoryEntry id="a7bb-d807-775b-67a3" name="Primary army: Solar Auxilia" hidden="true"/>
    <categoryEntry id="422d-1a0b-703f-b8be" name="Primary army: Mechanicum Taghmata" hidden="true"/>
    <categoryEntry id="9058-983e-c324-62a4" name="Primary army: Legio Titanicus" hidden="true"/>
    <categoryEntry id="26a2-ea6d-4d79-445f" name="Primary army: Knight Household" hidden="true"/>
    <categoryEntry id="ed05-1bd8-1e03-af1c" name="Primary army: Imperial Militia" hidden="true"/>
    <categoryEntry id="1c10-b820-4588-74dd" name="Primary army: Daemons Of The Ruinstorm" hidden="true"/>
    <categoryEntry id="fbc3-4530-e34d-3e92" name="Primary army: Legion Astartes (core list)" hidden="true"/>
    <categoryEntry id="027f-543a-9ab7-362f" name="Primary army: Legion Astartes (Iron Hands)" hidden="true"/>
    <categoryEntry id="cdb7-8175-d8f5-e789" name="Primary army: Legion Astartes (Raven Guard)" hidden="true"/>
    <categoryEntry id="0e75-595f-c943-9de7" name="Primary army: Legion Astartes (Salamanders)" hidden="true"/>
    <categoryEntry id="9f63-b141-7da9-b4a9" name="Primary army: Legion Astartes (Ultramarines)" hidden="true"/>
    <categoryEntry id="a914-8960-4425-06b1" name="Primary army: Legion Astartes (Imperial Fists)" hidden="true"/>
    <categoryEntry id="d300-75be-c303-5ebb" name="Primary army: Legion Astartes (Blood Angels)" hidden="true"/>
    <categoryEntry id="3162-8794-c22f-7807" name="Primary army: Legion Astartes (Dark Angels)" hidden="true"/>
    <categoryEntry id="d037-4311-962d-1cd1" name="Primary army: Legion Astartes (White Scars)" hidden="true"/>
    <categoryEntry id="2fc6-7090-5156-e67b" name="Primary army: Legion Astartes (Space Wolves)" hidden="true"/>
    <categoryEntry id="e0d0-2698-7314-b6b3" name="Primary army: Legion Astartes (Night Lords)" hidden="true"/>
    <categoryEntry id="4475-2bda-6380-001c" name="Primary army: Legion Astartes (World Eaters)" hidden="true"/>
    <categoryEntry id="90e7-0b6b-eacd-a5ee" name="Primary army: Legion Astartes (Emperor's Children)" hidden="true"/>
    <categoryEntry id="ddfc-8dee-03f2-0f39" name="Primary army: Legion Astartes (Iron Warriors)" hidden="true"/>
    <categoryEntry id="3ee5-34f0-b818-8a51" name="Primary army: Legion Astartes (Death Guard)" hidden="true"/>
    <categoryEntry id="8d15-2339-9ba7-4154" name="Primary army: Legion Astartes (Word Bearers)" hidden="true"/>
    <categoryEntry id="0741-f83d-1df8-9c36" name="Primary army: Legion Astartes (Sons of Horus)" hidden="true"/>
    <categoryEntry id="158a-6d8f-110a-3929" name="Primary army: Legion Astartes (Alpha Legion)" hidden="true"/>
    <categoryEntry id="8e75-5c6e-2a7f-54dc" name="Primary army: Legion Astartes (Thousand Sons)" hidden="true"/>
    <categoryEntry id="813c-67a8-ed81-24f9" name="Not an allowed ally of the primary army" hidden="false"/>
  </categoryEntries>
  <selectionEntries>
    <selectionEntry id="a361-b07f-1b9c-872c" name="Allow fan-made units" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="2848-b95e-0e3b-bb33" type="max"/>
      </constraints>
      <rules>
        <rule id="b85c-31ef-bd96-d0b9" name="Allow fan-made units" hidden="false">
          <description>Shows fan-made units and options that are not part of EpicAU (see the README for their sources). Taking it in any force shows them in every force of the roster; removing it flags any that were taken. Legion Astartes: Legion Arquitor Bombard Squadron, Legion Tarantula Battery, Legion Kratos Heavy Tank Squadron, Sicaran Punisher, Sicaran Arcus. Legio Titanicus: Warbringer Nemesis Titan, Warmaster Titan.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="0c5b-2a27-0bea-2968" name="Configuration" hidden="false" targetId="ba14-d0f1-f942-df54" primary="true"/>
      </categoryLinks>
    </selectionEntry>
  </selectionEntries>
  <sharedRules>
    <rule id="d6db-799f-23f8-2194" name="Allies" hidden="false">
      <description>Formations from a Disruptive ally reduce the army's strategy rating by 1, and Supreme Commander re-rolls cannot be used on them. Allied formations follow their own list's restrictions (an allied Line Detachment is needed before an allied Support Detachment). Spacecraft and Supreme Commander limits apply across the whole army; only one Supreme Commander may be taken and it must come from the primary list.</description>
    </rule>
    <rule id="0be9-a6dd-0220-503a" name="Armorbane" hidden="false">
      <description>Hits from this weapon's AT, CC or FF value reduce the target's save by 1 when allocated to LV, AV or WE units. No effect against INF.</description>
    </rule>
    <rule id="af85-62be-8c26-d32c" name="Armoured Spearhead" hidden="false">
      <description>The army may garrison one formation made up only of AV units per full 2000 points, ignoring the usual garrison restrictions. These formations may start on overwatch but count towards the normal limit of garrisoned formations on overwatch.</description>
    </rule>
    <rule id="51c1-f555-6f26-9861" name="Berserk" hidden="false">
      <description>The unit may double its move when taking an Engage action.</description>
    </rule>
    <rule id="5a4c-99c2-45f6-5795" name="Brutal" hidden="false">
      <description>When a formation containing Brutal units wins an assault, it counts one extra hit when working out hack-downs. This does not help decide who won the assault.</description>
    </rule>
    <rule id="0d2f-03cf-5568-06f5" name="Chain of Command" hidden="false">
      <description>The army may add one free Lieutenant Commander per full 1000 points to formations able to take the Praetor upgrade. Each counts towards that formation's upgrade limit and cannot join a formation with another Praetor upgrade; unused ones are lost.</description>
    </rule>
    <rule id="a32b-c2cb-bc57-6904" name="Demi-God" hidden="false">
      <description>Has three wounds and may be allocated hits up to its starting wounds. Must stay within 5cm of its formation unless it has Scout. Needs two Blast markers to be suppressed or broken, takes no Blast marker for losing a wound, suffers no critical hits and cannot barge. When destroyed, every friendly formation within 30cm takes two Blast markers. Counts as its retinue's unit type for transport.</description>
    </rule>
    <rule id="75bb-a312-d4d2-5b25" name="Exploratory Augury Web" hidden="false">
      <description>Friendly units arriving by Teleport within 15cm of this unit do not roll for Blast markers.</description>
    </rule>
    <rule id="e977-24ca-df0a-2945" name="Feedback" hidden="false">
      <description>If the weapon hits but causes no damage, roll a D6 for each successful save the target made; the firing unit takes a Blast marker for each 1.</description>
    </rule>
    <rule id="4700-411c-f590-06ef" name="Ferocity" hidden="false">
      <description>The unit adds 5cm to its counter-charge move in an assault.</description>
    </rule>
    <rule id="2bb4-5124-ca44-774e" name="Fleshbane" hidden="false">
      <description>Hits from this weapon's AP, CC or FF value reduce the target's save by 1 when allocated to INF or LV units. No effect against AV or WE.</description>
    </rule>
    <rule id="30d6-dddf-d298-0f34" name="Lance" hidden="false">
      <description>AV units with Reinforced Armour may not re-roll saves against hits from this weapon. No effect against INF or LV.</description>
    </rule>
    <rule id="a6b2-6364-a6e6-8d1d" name="Legion Astartes" hidden="false">
      <description>Two Blast markers are needed to suppress a unit or kill one in a broken formation. The formation breaks at two Blast markers per unit, counts half its Blast markers (rounded down) in assault resolution, takes Blast markers equal to its units (not half) when it rallies, and Leaders remove 2 Blast markers instead of 1.</description>
    </rule>
    <rule id="cdd5-87d5-df9f-9349" name="Macro-Weapon" hidden="false">
      <description>Targets get no save unless they have Reinforced Armour or an Invulnerable Save, and even then cannot re-roll. Only applies to the unit type matching the to-hit value used.</description>
    </rule>
    <rule id="1c5a-eb38-f506-2b8b" name="Remorseless" hidden="false">
      <description>A broken formation suffers only -1 (not -2) to its rally roll for being broken.</description>
    </rule>
    <rule id="d4c1-724d-bbcb-8056" name="Siege" hidden="false">
      <description>The weapon counts as a Macro-Weapon against units with 0cm speed.</description>
    </rule>
    <rule id="9d1d-6151-5a53-1044" name="Singularity" hidden="false">
      <description>Each unmodified to-hit roll of 6 generates another attack dice; further 6s keep generating dice.</description>
    </rule>
    <rule id="e5cd-d8ff-75bb-52b4" name="Sniper" hidden="false">
      <description>Roll to hit separately for sniper attacks; hits may be allocated to any valid target the attacker chooses.</description>
    </rule>
    <rule id="b807-4dc8-c02d-988b" name="Void Shields" hidden="false">
      <description>Each shield stops one point of damage before saves and Blast markers, then goes down. Close combat hits ignore shields; firefight hits must knock them down first. One downed shield is repaired each end phase, and a regroup roll can repair shields instead of removing Blast markers.</description>
    </rule>
    <rule id="262a-595f-46af-5c10" name="The Emperor's Chosen" hidden="false">
      <description>As Legion Astartes (two Blast markers to suppress or kill when broken, break at two Blast markers per unit, half Blast markers in assault resolution, full Blast markers on rallying, Leaders remove 2). In addition, Legio Custodes formations halve the hack-downs they suffer after losing an assault.</description>
    </rule>
    <rule id="7a75-4235-9819-0fe3" name="Automaton" hidden="false">
      <description>The formation takes no Blast marker when this unit is destroyed (including crossfire and out-of-coherency losses). Disrupt hits still place Blast markers. Hits from Blast markers on a broken formation may be saved normally.</description>
    </rule>
    <rule id="dc68-8e9b-a532-5ad8" name="Cortex Controller" hidden="false">
      <description>Formations with Cybernetica Cortex units operate normally if they have a unit within 15cm of a unit with this rule.</description>
    </rule>
    <rule id="8d61-66bd-1c1d-5a6c" name="Cybernetica Cortex" hidden="false">
      <description>Unless a friendly Cortex Controller is within 15cm, the formation suffers -1 initiative and may not March or Overwatch.</description>
    </rule>
    <rule id="271b-4070-ab46-9c05" name="Ion Gauntlet" hidden="false">
      <description>4+ save against normal, MW and TK shooting and firefight hits, and 5+ against normal, MW and TK close combat hits. Each point of TK damage is saved separately. Failed saves may still use Reinforced Armour where allowed. Not usable in a crossfire.</description>
    </rule>
    <rule id="db8a-9a85-3182-f8d3" name="Ion Shield" hidden="false">
      <description>4+ save against normal, MW and TK shooting and firefight hits. Each point of TK damage is saved separately. Failed saves may still use Reinforced Armour where allowed. Not usable in a crossfire.</description>
    </rule>
    <rule id="21f7-881b-3b30-8c21" name="Instability" hidden="false">
      <description>A Daemonic Horde that fails an initiative test loses D3 Lesser Daemon (INF) units. These losses cause no Blast markers but can break the formation.</description>
    </rule>
    <rule id="3d90-f4d8-85bc-dca9" name="Chaos Gate" hidden="false">
      <description>Up to three detachments may be kept in the Warp and enter play through the Gate, measuring their first move from its centre. Only one detachment may come through each turn.</description>
    </rule>
    <rule id="1ce2-f7e0-7be5-11f3" name="Daemonic Assault" hidden="false">
      <description>Before deployment, nominate one detachment per full 1000 points (or per 1000 points of allied allowance) to arrive by Teleport from turn two. Each may contain only one Greater Daemon.</description>
    </rule>
    <rule id="b4b1-8c7e-039b-d41d" name="Provenance" hidden="false">
      <description>Applies to all INF units in the formation. Warrior Elite: +1 FF. Survivors of the Dark Age: +1 armour save. Feral Warriors: +1 CC. Traitors: Berserk. Only two Provenance types may be used across the army.</description>
    </rule>
    <rule id="199e-8a5d-36e8-ccc4" name="Discipline Masters / Rogue Psykers" hidden="false">
      <description>One free Discipline Master (or Rogue Psyker) per 500 points or part thereof, added before set-up. The first must join the Force Commander's formation, or the most expensive Imperial Militia formation if there is no Force Commander.</description>
    </rule>
    <rule id="59fb-d336-6931-c7ba" name="Legate Commander" hidden="false">
      <description>One free Legate Commander per 500 points or part thereof. If the army has a Lord Marshall, the first joins the Lord Marshall's formation. No more than one per formation, and none in Imperial Navy or allied formations; excess Legates are lost.</description>
    </rule>
    <rule id="68a3-1fb7-9d48-7742" name="Dedicated War Engine Transports" hidden="false">
      <description>Gorgon, Dracosan and Stormlord transports may only carry units from their own formation; the normal war engine transport rules do not apply.</description>
    </rule>
    <rule id="b96b-f873-e508-4308" name="Drop Assault" hidden="false">
      <description>The formation is transported in Drop Pods (Planetfall) at no cost.</description>
    </rule>
    <rule id="f8ed-bf3a-efe7-098f" name="Teleport" hidden="false">
      <description>Core Epic Armageddon rule: the unit may deploy by teleporting onto the battlefield, rolling for Blast markers on arrival.</description>
    </rule>
    <rule id="2daa-1b22-93f8-fbec" name="Knight Household" hidden="false">
      <description>Formations get +1 to action tests when taking an Engage action and +1 to rally tests.</description>
    </rule>
    <rule id="4927-be7a-ebf9-a1cf" name="Reinforced Armour" hidden="false">
      <description>Core rule: may re-roll a failed save, except against Macro-Weapons, Titan Killers or in a crossfire.</description>
    </rule>
    <rule id="c562-9990-f721-32fb" name="Thick Rear Armour" hidden="false">
      <description>Core rule: crossfire does not reduce this unit's save.</description>
    </rule>
    <rule id="3826-e379-3e86-c292" name="Invulnerable Save" hidden="false">
      <description>Core rule: gets a 6+ save (or the value listed) even when no save would normally be allowed.</description>
    </rule>
    <rule id="f378-6c2c-d474-1f3d" name="Walker" hidden="false">
      <description>Core rule: may re-roll failed dangerous terrain tests.</description>
    </rule>
    <rule id="27df-3871-dea6-a839" name="Skimmer" hidden="false">
      <description>Core rule: may hover over terrain and pop up; can only be hit in assault by units able to engage skimmers.</description>
    </rule>
    <rule id="1409-373f-7ba8-c148" name="Scout" hidden="false">
      <description>Core rule: may deploy forward and has a wider zone of control and coherency spacing.</description>
    </rule>
    <rule id="f14b-f1e8-683e-cd73" name="Infiltrator" hidden="false">
      <description>Core rule: may double its move when taking an Engage action and ignores enemy zones of control when doing so.</description>
    </rule>
    <rule id="2971-9d24-65e8-a53e" name="Jump Packs" hidden="false">
      <description>Core rule: may move over terrain and other units as if skimming.</description>
    </rule>
    <rule id="4357-7618-ea64-6347" name="Mounted" hidden="false">
      <description>Core rule: counts as a vehicle for terrain purposes while remaining INF.</description>
    </rule>
    <rule id="aba9-b846-28f1-57e0" name="Fearless" hidden="false">
      <description>Core rule: not destroyed by Blast markers when broken and not killed by hack-downs.</description>
    </rule>
    <rule id="5455-b041-3489-bee6" name="Leader" hidden="false">
      <description>Core rule: removes an extra Blast marker when the formation rallies or marshals.</description>
    </rule>
    <rule id="4c56-05fb-87be-3e8a" name="Commander" hidden="false">
      <description>Core rule: may bring in up to three formations within 5cm when it takes an Engage action.</description>
    </rule>
    <rule id="d94c-8ff7-0b2a-e614" name="Supreme Commander" hidden="false">
      <description>Core rule: as Commander, plus one re-roll per turn for a failed initiative test.</description>
    </rule>
    <rule id="7308-eebe-f5c9-137b" name="Inspiring" hidden="false">
      <description>Core rule: each unit counts as an extra unit when working out assault resolution modifiers.</description>
    </rule>
    <rule id="6a98-a141-f09e-3c89" name="Planetfall" hidden="false">
      <description>Core rule: may enter play from orbit using a planetfall move.</description>
    </rule>
    <rule id="3f9e-9cb4-20b7-6736" name="Transport" hidden="false">
      <description>Core rule: carries the listed units.</description>
    </rule>
    <rule id="392f-db6b-487f-fe1a" name="Indirect Fire" hidden="false">
      <description>Core rule: may fire at targets out of line of fire at reduced range and without sustained-fire bonuses.</description>
    </rule>
    <rule id="0c8c-0dee-e0e3-4837" name="Ignore Cover" hidden="false">
      <description>Core rule: targets get no cover save modifiers.</description>
    </rule>
    <rule id="e9e3-ad45-1546-7db4" name="Disrupt" hidden="false">
      <description>Core rule: every hit places a Blast marker even if saved.</description>
    </rule>
    <rule id="c8b5-a2a9-69b5-d152" name="Single Shot" hidden="false">
      <description>Core rule: may only be fired once per battle.</description>
    </rule>
    <rule id="fe36-0a82-a4ee-3f54" name="Slow Firing" hidden="false">
      <description>Core rule: may only fire every other turn.</description>
    </rule>
    <rule id="ed59-9ced-a699-b761" name="Titan Killer" hidden="false">
      <description>Core rule: each hit causes the listed number of damage points to a war engine.</description>
    </rule>
    <rule id="4b49-c4e2-b896-4689" name="Extra Attacks" hidden="false">
      <description>Core rule: grants the listed number of additional close combat or firefight attacks.</description>
    </rule>
    <rule id="d859-b0a0-af5c-bb73" name="First Strike" hidden="false">
      <description>The unit strikes first in an assault: its attacks are resolved, and casualties removed, before the enemy's.</description>
    </rule>
    <rule id="b2c9-ae47-ce23-0fa6" name="Small Arms" hidden="false">
      <description>Core rule: a weapon shown in brackets with (small arms) is only used in firefights, adding its listed abilities and Extra Attacks to the unit's FF attacks. It cannot shoot in the shooting phase.</description>
    </rule>
    <rule id="5d5a-3534-a8bf-4935" name="Assault Weapons" hidden="false">
      <description>Core rule: a weapon marked (assault weapons) is used in close combat, adding its listed abilities and Extra Attacks to the unit's CC attacks.</description>
    </rule>
    <rule id="f379-0377-5661-ed26" name="Barrage" hidden="false">
      <description>Core rule: BP weapons place Barrage templates instead of rolling to hit normally. The number of Barrage Points sets how many templates are placed and what is needed to hit the units under them.</description>
    </rule>
    <rule id="8f11-c190-ff78-a7d6" name="Fixed Forward Fire Arc" hidden="false">
      <description>Core rule (FxF): the weapon may only target units in a 90-degree arc straight ahead of the unit.</description>
    </rule>
    <rule id="e787-7eab-2cba-d6f0" name="Forward Fire Arc" hidden="false">
      <description>Core rule (Fwd): the weapon may only target units in the 180-degree arc to the unit's front.</description>
    </rule>
    <rule id="e953-40ea-7719-e17c" name="Rear Fire Arc" hidden="false">
      <description>Core rule: the weapon may only target units in the 180-degree arc to the unit's rear.</description>
    </rule>
    <rule id="8fd7-7a53-db8a-8526" name="Left Fire Arc" hidden="false">
      <description>Core rule (LF): the weapon may only target units in the arc to the unit's left side.</description>
    </rule>
    <rule id="24b1-8727-a5a1-0b4b" name="Right Fire Arc" hidden="false">
      <description>Core rule (RF): the weapon may only target units in the arc to the unit's right side.</description>
    </rule>
    <rule id="b2d2-de55-191a-358d" name="Damage Capacity" hidden="false">
      <description>Core rule (DC): a war engine has this many damage points. Each unsaved hit removes one and it is destroyed at zero. War engines can also take critical hits.</description>
    </rule>
    <rule id="f048-04fb-786f-b4e5" name="Critical Hits" hidden="false">
      <description>Core rule: some damage against a war engine causes a critical hit. The effect for each unit is given in its notes.</description>
    </rule>
    <rule id="931d-35b7-00f9-bfd2" name="Slow and Steady" hidden="false">
      <description>Spacecraft with this rule may not be used in the opening turn(s) of a battle stated in their notes, unless the scenario says otherwise.</description>
    </rule>
    <rule id="589c-8651-5655-a06b" name="Fortifications" hidden="false">
      <description>Static defences with 0cm speed; Siege weapons count as Macro-Weapons against them. The EpicAU fortifications page was not archived.</description>
    </rule>
    <rule id="b2b1-6882-acb7-9daa" name="Secondary Targeting Protocols" hidden="false">
      <description>Listed on the experimental Emperor-class Titans but not defined on the archived EpicAU wiki.</description>
    </rule>
  </sharedRules>
</gameSystem>
