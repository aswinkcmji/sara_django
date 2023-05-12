package main
import (
    "database/sql"
    "fmt"
    _ "github.com/lib/pq"
    "github.com/jasonlvhit/gocron"
    // "gopkg.in/robfig/cron.v2"
)
const (
    host     = "localhost"
    port     = 5432
    user     = "django"
    password = "eps19"
    dbname   = "django"
  )


  func fetchUsers_id(db *sql.DB)  {


	var bonus float64

	rows, err := db.Query(
		`select * from "adminPanel_queuemodel" order by id asc limit 1 `)
	//fmt.Println("Fetching users...")
	if err != nil {
		panic(err)
		}
	defer rows.Close()
	id:=""
	username:=""
	sponsor:=""
	var totalprice float64
	for rows.Next(){  
		rows.Scan(&id,&username,&sponsor,&totalprice)
		fmt.Println("\n", id,"\n",username,"\n",sponsor,"\n",totalprice,"\n")

	}

	// bonus:=0

	rows2 := db.QueryRow(
	`select badge from "adminPanel_newusermodel" where username = $1`,sponsor)
	
	cbadge:=0
	rows2.Scan(&cbadge)
	// fmt.Println( "\n current-badge", cbadge )



	// fetching bafhe details 
	rows3, err := db.Query(
		`select sponsorbonus from "adminPanel_badgedetailsmodel" where badge = $1`,cbadge)
	if err != nil {
		panic(err)
		}
	defer rows3.Close()
	var bamount float64
	for rows3.Next(){  

		rows3.Scan(&bamount)
	
	}
	// fmt.Println( "\n bonus amount", bamount )
	



	
	if sponsor == "admin" {
		_,er := db.Exec(
			`delete from "adminPanel_queuemodel" where username = $1`,username)
	if er != nil {
		panic(er)
		}

		
	}else if username != ""{
		switch cbadge {
		
		case 0:

      bonus = (totalprice * bamount)/100
			fmt.Println("\n bonus", bonus)
      
			var cbonus,totalbonus,wallet,totalwallet,adminwallet,admin float64
			
      row := db.QueryRow(`select bonus from "adminPanel_newusermodel" where username = $1`, sponsor)
			
			row.Scan(&cbonus)

      rows := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, sponsor)
						
			rows.Scan(&wallet)

      rows1 := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, "admin")
						
			rows1.Scan(&admin)

			totalbonus = cbonus + bonus

      totalwallet = wallet + bonus

      adminwallet = admin - bonus

			_,e := db.Exec(
				`update "adminPanel_newusermodel" set bonus = $1,wallet = $2 where username = $3`,totalbonus,totalwallet,sponsor)
			fmt.Println("Fetching users...")
			if e != nil {
				panic(e)
				}

      _,err := db.Exec(
        `update "adminPanel_newusermodel" set wallet = $1 where username =$2`,adminwallet,"admin")
      fmt.Println("Fetching users...")
      if err != nil {
        panic(err)
        }
			_,e1r := db.Exec(
				`INSERT INTO "adminPanel_bonushistorymodel" (username,sponsor,bonusamount,purchasedamount) VALUES ($1,$2,$3,$4)`,username,sponsor,bonus,totalprice)
			if e1r != nil {
				panic(e1r)
			}

			_,er := db.Exec(
					`delete from "adminPanel_queuemodel" where username = $1`,username)
			if er != nil {
				panic(er)
				}
			fmt.Println("DIAMOND")
            break

		case 1:

      bonus = (totalprice * (bamount/100))
			fmt.Println("\n bonus", bonus)
      
			var cbonus,totalbonus,wallet,totalwallet,adminwallet,admin float64
			
      row := db.QueryRow(`select bonus from "adminPanel_newusermodel" where username = $1`, sponsor)
			
			row.Scan(&cbonus)

      rows := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, sponsor)
						
			rows.Scan(&wallet)

      rows1 := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, "admin")
						
			rows1.Scan(&admin)

			totalbonus = cbonus + bonus

      totalwallet = wallet + bonus

      adminwallet = admin - bonus

			_,e := db.Exec(
				`update "adminPanel_newusermodel" set bonus = $1,wallet = $2 where username = $3`,totalbonus,totalwallet,sponsor)
			fmt.Println("Fetching users...")
			if e != nil {
				panic(e)
				}

      _,err := db.Exec(
        `update "adminPanel_newusermodel" set wallet = $1 where username =$2`,adminwallet,"admin")
      fmt.Println("Fetching users...")
      if err != nil {
        panic(err)
        }
			_,e1r := db.Exec(
				`INSERT INTO "adminPanel_bonushistorymodel" (username,sponsor,bonusamount,purchasedamount) VALUES ($1,$2,$3,$4)`,username,sponsor,bonus,totalprice)
			if e1r != nil {
				panic(e1r)
			}
			_,er := db.Exec(
					`delete from "adminPanel_queuemodel" where username = $1`,username)
			if er != nil {
				panic(er)
				}
			fmt.Println("DIAMOND")
            break

			
		case 2:

      bonus = (totalprice * (bamount/100))
			fmt.Println("\n bonus", bonus)
      
			var cbonus,totalbonus,wallet,totalwallet,adminwallet,admin float64
			
      row := db.QueryRow(`select bonus from "adminPanel_newusermodel" where username = $1`, sponsor)
			
			row.Scan(&cbonus)

      rows := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, sponsor)
						
			rows.Scan(&wallet)

      rows1 := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, "admin")
						
			rows1.Scan(&admin)

			totalbonus = cbonus + bonus

      totalwallet = wallet + bonus

      adminwallet = admin - bonus

			_,e := db.Exec(
				`update "adminPanel_newusermodel" set bonus = $1,wallet = $2 where username = $3`,totalbonus,totalwallet,sponsor)
			fmt.Println("Fetching users...")
			if e != nil {
				panic(e)
				}

      _,err := db.Exec(
        `update "adminPanel_newusermodel" set wallet = $1 where username =$2`,adminwallet,"admin")
      fmt.Println("Fetching users...")
      if err != nil {
        panic(err)
        }
			

			_,e1r := db.Exec(
				`INSERT INTO "adminPanel_bonushistorymodel" (username,sponsor,bonusamount,purchasedamount) VALUES ($1,$2,$3,$4)`,username,sponsor,bonus,totalprice)
			if e1r != nil {
				panic(e1r)
			}
			_,er := db.Exec(
					`delete from "adminPanel_queuemodel" where username = $1`,username)
			if er != nil {
				panic(er)
				}
			fmt.Println("DIAMOND")
            break
		case 3:

      bonus = (totalprice * (bamount/100))
			fmt.Println("\n bonus", bonus)
      
			var cbonus,totalbonus,wallet,totalwallet,adminwallet,admin float64
			
      row := db.QueryRow(`select bonus from "adminPanel_newusermodel" where username = $1`, sponsor)
			
			row.Scan(&cbonus)

      rows := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, sponsor)
						
			rows.Scan(&wallet)

      rows1 := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, "admin")
						
			rows1.Scan(&admin)

			totalbonus = cbonus + bonus

      totalwallet = wallet + bonus

      adminwallet = admin - bonus

			_,e := db.Exec(
				`update "adminPanel_newusermodel" set bonus = $1,wallet = $2 where username = $3`,totalbonus,totalwallet,sponsor)
			fmt.Println("Fetching users...")
			if e != nil {
				panic(e)
				}

      _,err := db.Exec(
        `update "adminPanel_newusermodel" set wallet = $1 where username =$2`,adminwallet,"admin")
      fmt.Println("Fetching users...")
      if err != nil {
        panic(err)
        }
			

			_,e1r := db.Exec(
				`INSERT INTO "adminPanel_bonushistorymodel" (username,sponsor,bonusamount,purchasedamount) VALUES ($1,$2,$3,$4)`,username,sponsor,bonus,totalprice)
			if e1r != nil {
				panic(e1r)
			}
			_,er := db.Exec(
					`delete from "adminPanel_queuemodel" where username = $1`,username)
			if er != nil {
				panic(er)
				}
			fmt.Println("DIAMOND")
            break
			
		case 4:

			bonus = (totalprice * (bamount/100))
			fmt.Println("\n bonus", bonus)
      
			var cbonus,totalbonus,wallet,totalwallet,adminwallet,admin float64
			
      row := db.QueryRow(`select bonus from "adminPanel_newusermodel" where username = $1`, sponsor)
			
			row.Scan(&cbonus)

      rows := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, sponsor)
						
			rows.Scan(&wallet)

      rows1 := db.QueryRow(`select wallet from "adminPanel_newusermodel" where username = $1`, "admin")
						
			rows1.Scan(&admin)

			totalbonus = cbonus + bonus

      totalwallet = wallet + bonus

      adminwallet = admin - bonus

			_,e := db.Exec(
				`update "adminPanel_newusermodel" set bonus = $1,wallet = $2 where username = $3`,totalbonus,totalwallet,sponsor)
			fmt.Println("Fetching users...")
			if e != nil {
				panic(e)
				}

      _,err := db.Exec(
        `update "adminPanel_newusermodel" set wallet = $1 where username =$2`,adminwallet,"admin")
      fmt.Println("Fetching users...")
      if err != nil {
        panic(err)
        }
			


			_,e1r := db.Exec(
				`INSERT INTO "adminPanel_bonushistorymodel" (username,sponsor,bonusamount,purchasedamount) VALUES ($1,$2,$3,$4)`,username,sponsor,bonus,totalprice)
			if e1r != nil {
				panic(e1r)
			}
			_,er := db.Exec(
					`delete from "adminPanel_queuemodel" where username = $1`,username)
			if er != nil {
				panic(er)
				}
			fmt.Println("DIAMOND")
            break
		default:
			break

	}
	}


	


}   

func main() {
    
  fmt.Println("Starting database")
  psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+"password=%s dbname=%s sslmode=disable",host, port, user, password, dbname)
  db, err := sql.Open("postgres", psqlInfo)
  if err != nil {
    panic(err)
  }
  defer db.Close()
  fmt.Println("Database created successfully")
    s := gocron.NewScheduler()
    s.Every(2).Seconds().Do(fetchUsers_id,db)
    <- s.Start()
}
