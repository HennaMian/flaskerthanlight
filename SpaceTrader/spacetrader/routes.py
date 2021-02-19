"""Create app routing"""
import unicodedata
import random
from flask import render_template, url_for, request, flash, redirect
from spacetrader import app, db
from spacetrader.models import Player, Region
from spacetrader.models import Game, Universe, Ship, NPC
from spacetrader.forms import PlayerInfo

DESCRIPTION = [
    {
        'author': 'Flasker Than Light',
        'title': 'WELCOME TO SPACE TRADER',
        'content': 'A classic strategy video game about space travel and exploration',
        'date_posted': 'September 18, 2019'
    }
]

@app.route('/')
@app.route('/home')
def hello_world():
    """Renders template."""
    return render_template('home.html', posts=DESCRIPTION)


@app.route('/config', methods=['GET', 'POST'])
def about():
    """Creates all main player and game info; game object, essentially."""
    form = PlayerInfo()

    db.drop_all()
    db.create_all()

    if form.validate_on_submit():

        start_credits = 0
        if form.difficulty.data == 'Easy':
            start_credits = 1000
        elif form.difficulty.data == 'Medium':
            start_credits = 500
        elif form.difficulty.data == 'Hard':
            start_credits = 100

        game_1 = Game(difficulty=form.difficulty.data, pname=form.name.data,
                      pilotskill=form.pilotskillpoints.data,
                      fighterskill=form.fighterskillpoints.data,
                      merchantskill=form.merchantskillpoints.data,
                      engineerskill=form.engineerskillpoints.data,
                      credits=start_credits)

        db.session.add(game_1)
        db.session.commit()

        flash('Player Info Entered', 'success')
        return redirect(url_for('display', name=form.name.data, difficulty=form.difficulty.data,
                                pskillpoints=form.pilotskillpoints.data,
                                fskillpoints=form.fighterskillpoints.data,
                                mskillpoints=form.merchantskillpoints.data,
                                eskillpoints=form.engineerskillpoints.data,
                                startcredits=start_credits))

    return render_template('config.html', title='Initial Configuration Page', form=form)


@app.route('/display', methods=['GET', 'POST'])
def display():
    """displays all game info to user."""
    return render_template('display.html', name=request.args.get('name'),
                           difficulty=request.args.get('difficulty'),
                           pskillpoints=request.args.get('pskillpoints'),
                           fskillpoints=request.args.get('fskillpoints'),
                           mskillpoints=request.args.get('mskillpoints'),
                           eskillpoints=request.args.get('eskillpoints'),
                           startcredits=request.args.get('startcredits'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    """
    Creates playable game.
    """
    playerp = Player.query.first()
    reg = Region.query.filter_by(rname=playerp.curr_region).first()
    regions = Region.query.all()
    universe_u = Universe.query.first()
    ship_1 = Ship.query.first()
    game_1 = Game.query.first()

    distances = []
    fuel_costs = []
    for region_r in regions:
        places = Universe.dist_between_regions(universe_u, reg.x_coor, reg.y_coor,
                                               region_r.x_coor, region_r.y_coor)
        distances.append(places)
        fuel_c = places / ((playerp.pilotskill)**2)
        fuel_costs.append(fuel_c)

    items = {}
    types = []
    game_winning_item = str(playerp.pname) + "'s Universe"
    types.extend(["Food", "Weapons", "Wood", "Fur", "Medicine", "Metal", "Silver",
                  "Spices", "Gold", "Computers", game_winning_item])

    cargo = sum(list(Universe.market_types.values()))
    ship_1.cargospace -= cargo
    db.session.commit()

    items = Region.generate_market(reg, items)
    buy_prices = Player.buy_prices(playerp, playerp.merchantskill, reg.techlevel)
    sell_prices = Player.sell_prices(playerp, playerp.merchantskill, reg.techlevel)

    if reg.rname == "Nidavellir":
        items = Region.add_item(reg, game_winning_item, items)
        buy_prices = Region.add_price(reg, game_winning_item, game_1.difficulty, buy_prices)


    return render_template('game.html', region=reg, game=Game.query.all(),
                           player=Player.query.all(),
                           universe=Universe.query.all(),
                           regions=Region.query.all(), distances=distances, ship=Ship.query.all(),
                           fuelcosts=fuel_costs, items=items, types=types,
                           inventory=Universe.market_types,
                           buyprices=buy_prices, sellprices=sell_prices)


@app.route('/region', methods=['GET', 'POST'])
def region():
    """
    This method defines region.
    """
    region_to_travel = request.form.get("regions")
    reg = Region.query.filter_by(rname=region_to_travel).first()

    destreg = str(request.args.get('destreg'))
    if reg is None:
        reg = Region.query.filter_by(rname=destreg).first()

    game_1 = Game.query.first()
    threshold = 0

    if game_1.difficulty == "Easy":
        threshold = 10
    elif game_1.difficulty == "Medium":
        threshold = 40
    else:
        threshold = 80

    p_test = random.randint(1, 101)

    regions = Region.query.all()
    playerp = Player.query.first()
    db.session.commit()
    universe_u = Universe.query.first()
    ship_s = Ship.query.first()

    game_winning_item = str(playerp.pname) + "'s Universe"

    if ship_s.health <= 0:
        flash('Your ship ran out of health! Game Over. You lose.', 'danger')
        return redirect(url_for('over'))

    distances = []
    fuel_costs = []
    can_travel = True

    regi = Region.query.filter_by(rname=playerp.curr_region).first()
    if reg is None:
        reg = regi
    chosen_fc = Universe.dist_between_regions(
        universe_u, regi.x_coor, regi.y_coor,
        reg.x_coor, reg.y_coor) / ((playerp.pilotskill)**2)

    if chosen_fc > ship_s.fuelcapacity:
        can_travel = False

    buy_or_sell = request.form.get("buyorsell")
    what = request.form.get("type")
    amount = request.form.get("amount")

    if buy_or_sell == "Buy":
        strwhat = unicodedata.normalize('NFKD', what).encode('ascii', 'ignore')
        i = Player.buy_prices(playerp, playerp.merchantskill, regi.techlevel)
        i = Region.add_price(regi, game_winning_item, game_1.difficulty, i)
        print(i)
        price = int(amount) * i[strwhat]
        its = {}
        its = Region.generate_market(regi, its)
        its = Region.add_item(regi, game_winning_item, its)

        if (price <= playerp.credits and its[strwhat] >= int(amount)
                and ship_s.cargospace >= int(amount)):

            print(strwhat)

            if strwhat == game_winning_item:
                flash('You just won the game by buying the universe!', 'success')
                return redirect(url_for('over'))

            playerp.credits -= price
            Universe.market_types[strwhat] += int(amount)
            its[strwhat] -= int(amount)
            ship_s.cargospace -= int(amount)
            db.session.commit()
            flash('Transaction Successful!', 'success')
        else:
            flash('Transaction Unsuccessful', 'danger')

    elif buy_or_sell == "Sell":
        strwhat = unicodedata.normalize('NFKD', what).encode('ascii', 'ignore')
        i = Player.sell_prices(playerp, playerp.merchantskill, regi.techlevel)
        its = {}
        its = Region.generate_market(regi, its)
        if Universe.market_types[strwhat] >= int(amount):
            price = i[what] * int(amount)
            playerp.credits += price
            its[strwhat] += int(amount)
            Universe.market_types[strwhat] -= int(amount)
            ship_s.cargospace += int(amount)
            db.session.commit()
            flash('Transaction Successful!', 'success')
        else:
            flash('Transaction Unsuccessful', 'danger')


    refuel_amount = request.form.get("fuel")

    if refuel_amount is not None:
        if int(refuel_amount) > 100:
            flash('You cannot get that much fuel back.', 'danger')
        else:
            curr_fuel = ship_s.fuelcapacity
            fuel_cost = Ship.refuel(ship_s, curr_fuel, int(refuel_amount))
            if playerp.credits >= fuel_cost:
                ship_s.fuelcapacity = int(refuel_amount)
                playerp.credits -= fuel_cost
                db.session.commit()
                flash('You successfully refueled!', 'success')
            else:
                flash('You cannot afford that much fuel.', 'danger')

    repair_amount = request.form.get("repair")

    if repair_amount is not None:
        if int(repair_amount) > 100:
            flash('You cannot get that much fuel back.', 'danger')
        else:
            eskill = playerp.engineerskill
            repair_cost = Ship.repair(ship_s, eskill)
            if playerp.credits >= repair_cost:
                ship_s.health = int(repair_amount)
                playerp.credits -= repair_cost
                db.session.commit()
                flash('You successfully repaired your ship!', 'success')
            else:
                flash('You cannot afford repairing to that health.', 'danger')

    if can_travel:

        returning = request.args.get('returning')

        if p_test < threshold and returning is None:
            player_inv = sum(Universe.market_types.values())

            ctype = ""
            if player_inv > 0:
                ctype = random.choice(["Bandit", "Police", "Trader"])
            else:
                ctype = random.choice(["Bandit", "Trader"])

            npc = NPC(ctype)
            db.session.add(npc)
            db.session.commit()
            if ctype == "Bandit":
                pay_amount = random.randint(40, 71)
                flash('Oh no! You have encountered a bandit!', 'warning')
                return redirect(url_for('bandit', ctype=ctype, amount=pay_amount,
                                        prev_reg=regi.rname, dest_reg=reg.rname))

            elif ctype == "Police":
                types = Universe.market_types.keys()
                stolen_type = random.choice(types)
                flash('Oh no! You have encountered police! They think you have stolen items',
                      'warning')
                return redirect(url_for('police', ctype=ctype, prev_reg=regi.rname,
                                        dest_reg=reg.rname, stolentype=stolen_type))

            num_items = random.randint(2, 11)
            item_type = random.choice(Universe.market_types.keys())
            price = num_items * 10
            flash('You have encountered a trader', 'warning')
            return redirect(url_for('trader', ctype=ctype, amount=num_items,
                                    itemtype=item_type, price=price, prev_reg=regi.rname,
                                    dest_reg=reg.rname))

        ship_s.fuelcapacity = ship_s.fuelcapacity - chosen_fc
        playerp.curr_region = reg.rname
        db.session.commit()
        items = {}
        types = []
        types.extend(["Food", "Weapons", "Wood", "Fur", "Medicine",
                      "Metal", "Silver", "Spices", "Gold", "Computers", game_winning_item])

        items = Region.generate_market(reg, items)
        buy_prices = Player.buy_prices(playerp, playerp.merchantskill, reg.techlevel)
        sell_prices = Player.sell_prices(playerp, playerp.merchantskill, reg.techlevel)

        if reg.rname == "Nidavellir":
            items = Region.add_item(reg, game_winning_item, items)
            buy_prices = Region.add_price(reg, game_winning_item, game_1.difficulty, buy_prices)

        for region_r in regions:
            places = Universe.dist_between_regions(universe_u, reg.x_coor, reg.y_coor,
                                                   region_r.x_coor, region_r.y_coor)
            distances.append(places)
            fuel_c = places / ((playerp.pilotskill)**2)
            fuel_costs.append(fuel_c)

        flash('You have successfully traveled to this region!', 'success')
        return render_template('region.html', distances=distances, region=reg,
                               regions=Region.query.all(), game=Game.query.all(),
                               universe=Universe.query.all(), player=Player.query.all(),
                               ship=Ship.query.all(),
                               fuelcosts=fuel_costs, items=items, types=types,
                               inventory=Universe.market_types, buyprices=buy_prices,
                               sellprices=sell_prices, returning=returning, destreg=destreg)

    playerp.curr_region = regi.rname
    db.session.commit()
    items = {}
    types = []
    types.extend(["Food", "Weapons", "Wood", "Fur", "Medicine", "Metal", "Silver",
                  "Spices", "Gold", "Computers", game_winning_item])

    items = Region.generate_market(regi, items)
    buy_prices = Player.buy_prices(playerp, playerp.merchantskill, regi.techlevel)
    sell_prices = Player.sell_prices(playerp, playerp.merchantskill, regi.techlevel)

    if regi.rname == "Nidavellir":
        items = Region.add_item(regi, game_winning_item, items)
        buy_prices = Region.add_price(regi, game_winning_item, game_1.difficulty, buy_prices)

    for region_r in regions:
        places = Universe.dist_between_regions(universe_u, regi.x_coor, regi.y_coor,
                                               region_r.x_coor, region_r.y_coor)
        distances.append(places)
        fuel_c = places / ((playerp.pilotskill)**2)
        fuel_costs.append(fuel_c)

    flash('You cannot travel to this region', 'danger')
    return render_template('region.html', distances=distances, region=regi,
                           regions=Region.query.all(), game=Game.query.all(),
                           universe=Universe.query.all(), player=Player.query.all(),
                           ship=Ship.query.all(), fuelcosts=fuel_costs, items=items,
                           types=types, inventory=Universe.market_types,
                           buyprices=buy_prices, sellprices=sell_prices,
                           destreg=destreg)


@app.route('/bandit', methods=['GET', 'POST'])
def bandit():
    """Displays bandit page."""
    decision = request.form.get("decide")

    player = Player.query.first()
    ship = Ship.query.first()
    pay_amount = request.args.get('amount')
    inventory = Universe.market_types.values()

    prevreg = str(request.args.get('prev_reg'))
    destreg = str(request.args.get('dest_reg'))

    if decision == "Pay":
        if int(player.credits) >= int(pay_amount):
            player.credits -= int(pay_amount)
            db.session.commit()
            flash("You paid the demanded amount", 'warning')
            return redirect(url_for('region', returning=True, destreg=destreg))
        else:
            if sum(inventory) > 0:
                ship.cargospace += sum(inventory)
                Universe.market_types = dict.fromkeys(Universe.market_types, 0)
                db.session.commit()
                flash("You lost gave the bandit all of your inventory.", 'danger')
                return redirect(url_for('region', returning=True, destreg=destreg))

            damage = random.randint(20, 41)
            ship.health -= damage
            db.session.commit()
            flash("You couldn't pay or offer anything, so you lost ship health.",
                  'danger')
            return redirect(url_for('region', returning=True, destreg=destreg))

    elif decision == "Flee":
        thresh = random.randint(0, 21)
        if (player.pilotskill * 2) > thresh:
            flash("You successfully fleed back!", 'success')
            return redirect(url_for('region', returning=True, destreg=prevreg))

        player.credits = 0
        damage = random.randint(20, 41)
        ship.health -= damage
        db.session.commit()
        flash("You failed to flee and paid the price. Your ship lost health.", 'danger')
        return redirect(url_for('region', returning=True, destreg=prevreg))

    elif decision == "Fight":
        thresh = random.randint(0, 21)
        if (player.fighterskill * 2) > thresh:
            add_credits = random.randint(30, 51)
            player.credits += add_credits
            db.session.commit()
            flash("You successfully fought the bandit and got some of their credits!", 'success')
            return redirect(url_for('region', returning=True, destreg=destreg))

        player.credits = 0
        damage = random.randint(20, 41)
        ship.health -= damage
        db.session.commit()
        flash("You lost the fight and paid the price. Your ship lost health.", 'danger')
        return redirect(url_for('region', returning=True, destreg=prevreg))

    return render_template('bandit.html', ctype=request.args.get('ctype'),
                           amount=request.args.get('amount'), prev_reg=prevreg, dest_reg=destreg)

@app.route('/police', methods=['GET', 'POST'])
def police():
    """Displays police page."""
    decision = request.form.get("decide")

    player = Player.query.first()
    ship = Ship.query.first()

    stolen_type = str(request.args.get('stolentype'))
    ctype = request.args.get('ctype')

    prevreg = str(request.args.get('prev_reg'))
    destreg = str(request.args.get('dest_reg'))

    if decision == "Forfeit":
        ship.cargospace += Universe.market_types[stolen_type]
        Universe.market_types[stolen_type] = 0
        db.session.commit()
        flash("You forfeited all of the items the police thought were stolen.", 'warning')
        return redirect(url_for('region', returning=True, destreg=destreg))

    elif decision == "Flee":
        thresh = random.randint(0, 21)
        if (player.pilotskill * 2) > thresh:
            flash("You successfully fleed back!", 'success')
            return redirect(url_for('region', returning=True, destreg=prevreg))

        damage = random.randint(20, 41)
        ship.health -= damage
        ship.cargospace += Universe.market_types[stolen_type]
        Universe.market_types[stolen_type] = 0
        player.money -= random.randint(20, 41)
        db.session.commit()
        flash(
            "You failed to flee. Your ship lost health, you lost all of the stolen items.",
            'danger')
        return redirect(url_for('region', returning=True, destreg=prevreg))

    elif decision == "Fight":
        thresh = random.randint(0, 21)
        if (player.fighterskill * 2) > thresh:
            flash("You successfully fought the bandit and got some of their credits!", 'success')
            return redirect(url_for('region', returning=True, destreg=destreg))

        damage = random.randint(20, 41)
        ship.health -= damage
        ship.cargospace += Universe.market_types[stolen_type]
        Universe.market_types[stolen_type] = 0
        player.money -= random.randint(20, 41)
        db.session.commit()
        flash(
            "You failed to flee. Your ship lost health, you lost all of the stolen items.",
            'danger')
        return redirect(url_for('region', returning=True, destreg=prevreg))

    return render_template('police.html', ctype=ctype, stolentype=stolen_type,
                           prev_reg=prevreg, dest_reg=destreg)

@app.route('/trader', methods=['GET', 'POST'])
def trader():
    """Displays trader page."""
    decision = request.form.get("decide")

    player = Player.query.first()
    ship = Ship.query.first()

    price = request.args.get('price')
    price = int(price)
    item_type = request.args.get('itemtype')
    amount = request.args.get('amount')
    ctype = request.args.get('ctype')

    prevreg = str(request.args.get('prev_reg'))
    destreg = str(request.args.get('dest_reg'))

    if decision == "Buy":
        player.credits -= int(price)
        ship.cargospace -= int(amount)
        Universe.market_types[str(item_type)] += int(amount)
        db.session.commit()
        flash("You bought the items!", 'success')
        return redirect(url_for('region', returning=True, destreg=destreg))

    elif decision == "Ignore":
        flash("You ignored the trader and kept travelling.", 'success')
        return redirect(url_for('region', returning=True, destreg=destreg))

    elif decision == "Rob":
        thresh = random.randint(0, 21)
        if (player.fighterskill * 2) > thresh:
            Universe.market_types[item_type] += int(amount)
            ship.cargospace -= int(amount)
            flash("You successfully robbed the trader!", 'success')
            return redirect(url_for('region', returning=True, destreg=destreg))

        damage = random.randint(20, 41)
        ship.health -= damage
        db.session.commit()
        flash("You failed to rob and paid the price. Your ship lost health.", 'danger')
        return redirect(url_for('region', returning=True, destreg=destreg))

    elif decision == "Negotiate":
        thresh = random.randint(0, 21)
        if (player.merchantskill * 2) > thresh:
            price /= 2
            flash("You successfully negotiated and brought the price down!", 'success')
        else:
            price *= 2
            flash("You tried to negotiate but failed. Now the price is even higher.", 'danger')

    return render_template('trader.html', ctype=ctype, amount=amount, itemtype=item_type,
                           price=price, prev_reg=prevreg, dest_reg=destreg)

@app.route('/over', methods=['GET', 'POST'])
def over():
    """Displays Game Over Page"""
    message = "GAME OVER"
    db.drop_all()
    return render_template('over.html', message=message)
