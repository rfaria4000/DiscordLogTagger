fightQuery = """
  query getReport($fightCode: String){
    reportData{
      report(code: $fightCode){
        masterData{
          actors{
            id
            name
            subType
          }
        }
        
        owner{
          name
        }
        startTime
        rankings
        
        fights(killType: Encounters){
          name
          id
          kill
          lastPhase
          bossPercentage
          fightPercentage
          startTime
          endTime
          difficulty
          friendlyPlayers
          encounterID
        }
      }
    }
  }
  """